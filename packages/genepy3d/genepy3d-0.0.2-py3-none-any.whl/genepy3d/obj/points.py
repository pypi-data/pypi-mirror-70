import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import numpy as np
import pandas as pd
import scipy.stats as scs

from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from genepy3d.util import plot as pl, geo

from pyevtk.hl import pointsToVTK

class Points:
    """Points cloud in 3D.
    
    Attributes:
        coors (2d array): list of 3d points.
    
    """
    def __init__(self, _coors):
        self.coors = _coors
    
    @classmethod
    def from_csv(cls,filepath,column_names=["x","y","z"],scales=(1.,1.,1.),args={}):
        """Constructor from csv file.
        
        Args:
            filepath (str): csv file.
            column_names (list of str): coordinates columns in csv file.
            scales (tuple of float): scales in x, y and z.
            args (dict): overried parameters of pandas.read_csv().
        
        Returns:
            Points.
        
        """
        
        # read file
        df = pd.read_csv(filepath,**args)
        
        # make lower case
        refined_column_names = [name.lower() for name in column_names]
        
        
        # extract all column names, remove irregular characters (e.g. space)
        # treat upper and lower cases as the same
        labels = df.columns.values
        refined_labels = []
        for lbl in labels:
            refined_labels.append(lbl.split()[0].lower())
        
        df.columns = refined_labels
            
        if all(lbl in refined_labels for lbl in refined_column_names):
            coors = df[refined_column_names].values / np.array(scales)
            return cls(coors)
        else:
            raise Exception("can not find column names in file.")
        
    
    def transform(self,phi=0,theta=0,psi=0,dx=0,dy=0,dz=0,zx=1,zy=1,zz=1):
        """Make transformation.
        
        Args:
            phi (float): rotation in x.
            theta (float): rotation in y.
            psi (float): rotation in z.
            dx (float): translation in x.
            dy (float): translation in y.
            dz (float): translation in z.
            zx (float): zoom in x.
            zy (float): zoom in y.
            zz (float): zoom in z.
        
        Returns:
            Points.
        
        """
        Pnew = self.coors.copy()
        Pnew = np.append(Pnew,np.ones((Pnew.shape[0],1)),axis=1) # add additional column for 3d transformation => [n, 4]
        Pnew = Pnew[:,:,np.newaxis] # add additional dimension for propagation of all points => [n, 4, 1]
        
        # translation
        Rt = np.array([
            [1., 0., 0., dx],
            [0., 1., 0., dy],
            [0., 0., 1., dz],
            [0., 0., 0., 1.],
        ])
        
        Pt = np.matmul(Rt,Pnew)
        
        # rotation in z
        Rpsi = np.array([
            [np.cos(psi), -np.sin(psi), 0., 0.],
            [np.sin(psi), np.cos(psi), 0., 0.],
            [0., 0., 1., 0.],
            [0., 0., 0., 1.],
        ])
        
        Pt = np.matmul(Rpsi,Pt)
        
        # rotation in y
        Rtheta = np.array([
            [np.cos(theta), 0, np.sin(theta), 0.],
            [0., 1., 0., 0.],
            [-np.sin(theta), 0., np.cos(theta), 0.],
            [0., 0., 0., 1.],
        ])
        
        Pt = np.matmul(Rtheta,Pt)
        
        # rotation in x
        Rphi = np.array([
            [1., 0., 0., 0.],
            [0., np.cos(phi), -np.sin(phi), 0.],
            [0., np.sin(phi), np.cos(phi), 0.],
            [0., 0., 0., 1.],
        ])
        
        Pt = np.matmul(Rphi,Pt)
        
        # zoom
        Rz = np.array([
            [zx, 0., 0., 0.],
            [0., zy, 0., 0.],
            [0., 0., zz, 0.],
            [0., 0., 0., 1.],
        ])
        
        Pt = np.matmul(Rz,Pt)
        
        return Points(Pt[:,:3,0])
    
    def fit_plane(self):
        """Fit plane.
            
        Returns:
            Tuple containing
                - c (float): intercept scalar.
                - normal (1d array): normal vector.
        
        """
        (rows, cols) = self.coors.shape
        G = np.ones((rows, 3))
        G[:, 0] = self.coors[:, 0]  #X
        G[:, 1] = self.coors[:, 1]  #Y
        Z = self.coors[:, 2]
        (a, b, c),resid,rank,s = np.linalg.lstsq(G, Z)
        normal = (a, b, -1)
        nn = np.linalg.norm(normal)
        normal = normal / nn
        
        return (c, normal)
    
    def pca(self):
        """Compute principal components analysis.
        
        Returns:
            Tuple containing
                - (1d array): empirical mean of points cloud.
                - (2d array): component vectors sorted by explained variance.
                - (2d array): explained variance.
        
        """
        
        pca=PCA(n_components=3)
        pca.fit(self.coors)
        return (pca.mean_,pca.components_,pca.explained_variance_)
    
    def test_isotropy(self,n_iter=100):
        """Isotropic test using bootstraping.
        
        Args:
            n_iter (int) : number of bootstraping iterations.
        
        Returns:
            p_value.
        
        """
        
        # PCA to collect explained variance        
        _, _, var = self.pca()
        vp1,vp2,vp3 = var
        
        # vp1/(vp1+vp2+vp3) proportion is near to 1/3 if the points cloud is isotropic.
        # Another proportion of the same type can be calculated with a spherical points
        # cloud which is a model of isotropic points cloud.
        # Simulating and calculating the second proportion several times allows to know
        # how much the studied sample is near to the model.
        t = vp1/(vp1+vp2+vp3)
        n_isotrop = 0.0
        
        for m in range(n_iter):
            n = len(self.coors)
            sphere = gen_sphere(n,1)
            _, _, svar = sphere.pca()
            ev1,ev2,ev3 = svar
            tprime = ev1/(ev1+ev2+ev3)
            if t <= tprime :
                n_isotrop += 1
        
        p_value = n_isotrop/n_iter
        
        return p_value
    
    def kmeans(self,**kwargs):
        """Clustering points cloud by the kmeans algorithm.
        
        Args:
            **kwargs : kmeans arguments in scikitlearn.
                                
        Returns:
            Tuple containing
                - labels (1d array): the integer label of each sample's point.
                - centers (2d array): the center of each cluster.
        
        """
        
        kmeans=KMeans(**kwargs)
        kmeans.fit(self.coors)
        labels=kmeans.predict(self.coors)
        centers=kmeans.cluster_centers_
        
        return (labels,centers)
    
    def to_CGAL(self):
        """Return the points as a list of CGAL Point_3 objects, for use in CGAL aglorithms.
                                
        Returns:
            a list of CGAL.Point_3 objects
        
        """
        
        from CGAL.CGAL_Kernel import Point_3
        
         #import CGAL? needs to be done from the caller, TODO: test that it's done
        return [Point_3(self.coors[i,0],self.coors[i,1],self.coors[i,2]) for i in range(len(self.coors))]

    def processs(self,removed_percentage = 5.0,nb_neighbors = 24, smooth=True):
        
        from CGAL.CGAL_Point_set_processing_3 import remove_outliers,jet_smooth_point_set

        pointsCgal=self.toCGAL()
         
        if removed_percentage:
            new_size=remove_outliers(pointsCgal, nb_neighbors, removed_percentage)
            pointsCgal=pointsCgal[0:new_size]
            
        if smooth:
            jet_smooth_point_set(pointsCgal,nb_neighbors)

        self.coors = np.array([[p.x(),p.y(),p.z()] for p in pointsCgal])

    def center(self):
        """Center the cloud to the mean of each coordinates.
                                                
        """
        self.coors[:,1]=self.coors[:,1]-self.coors[:,1].mean()
        self.coors[:,2]=self.coors[:,2]-self.coors[:,2].mean()
    
    def export_to_VTK(self,filepath):
        """Find the clusters of points cloud with the kmeans algorithm.
        
        Args:
            filepath (str): full path of file to save, without extention.
                                        
        """

        pointsToVTK(filepath, np.ascontiguousarray(self.coors[:,0]),  np.ascontiguousarray(self.coors[:,1]),  np.ascontiguousarray(self.coors[:,2]),data=None)

    def plot(self, ax, **kwds):
        """Plot points cloud.
        
        Args:
            ax: axis to be plotted.
            projection (str): support '3d'|'xy'|'xz'|'yz' plot.
            point_args (dic): matplotlib arguments for plotting points.
            equal_aspect (bool): make equal aspect for both axes.
        
        """
        
        if 'projection' in kwds.keys():
            projection = kwds['projection']
        else:
            projection = '3d'
        
        if 'equal_aspect' in kwds.keys():
            equal_aspect = kwds['equal_aspect']
        else:
            equal_aspect = True
            
        if 'point_args' in kwds.keys():
            point_args = kwds['point_args']
        else:
            point_args = {'color':'blue', 'alpha':0.9}

        x, y, z = self.coors[:,0], self.coors[:,1], self.coors[:,2]
        
        if projection == '3d':
            ax.scatter(x,y,z,**point_args)
            if equal_aspect == True:
                param = pl.fix_equal_axis(self.coors)
                ax.set_xlim(param['xmin'],param['xmax'])
                ax.set_ylim(param['ymin'],param['ymax'])
                ax.set_zlim(param['zmin'],param['zmax'])
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
        elif projection == 'xy':
            ax.scatter(x,y,**point_args)
            if equal_aspect == True:
                ax.axis('equal')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
        elif projection == 'xz':
            ax.scatter(x,z,**point_args)
            if equal_aspect == True:
                ax.axis('equal')
            ax.set_xlabel('X')
            ax.set_ylabel('Z')
        else:
            ax.scatter(y,z,**point_args)
            if equal_aspect == True:
                ax.axis('equal')
            ax.set_xlabel('Y')
            ax.set_ylabel('Z')

def emd(ps1, ps2, return_flows=False):
    """Compute Earth Mover's Distance (EMD) between two point clouds ps1, ps2.
    
    Args:
        ps1 (Points): point cloud.
        ps2 (Points): point cloud.
        return_flows (bool): if True then return maching flows between ps1 and ps2.
        
    Returns:
        EMD distance between ps1 and ps2 and if return_flows is True, then return array of matching flows.
    
    """
    
    return geo.emd(ps1.coors, ps2.coors, return_flows)

def gen_ellipsoid(axes_length=[1.,1.,1.],dtheta=np.pi/20,dphi=np.pi/20):
    """Generate point cloud on the surface of an ellipsoid. 
    
    Note that the points are not equally spaced.
    
    Args:
        axes_length (list of float): half length of the main axis along the three axes ([1.,1.,1.]) 
        dtheta (float): sampling along theta
        dphi (float): sampling along phi
    
    Returns:
        Points.
    
    """

    a=axes_length[0]
    b=axes_length[0]
    c=axes_length[0]
    
    theta=np.arange(0,2*np.pi,dtheta)
    phi=np.arange(0,2*np.pi,dphi)
    xel=[a*np.sin(t)*np.cos(p) for t in theta for p in phi]
    yel=[b*np.sin(t)*np.sin(p) for t in theta for p in phi]
    zel=[c*np.cos(t) for t in theta for p in phi]
    
    return Points(np.array([xel,yel,zel]).transpose())
 
def gen_gaussian_points(n=1000,center=[0,0,0],scales=1,orientation=[0,np.pi/2]):
    """Generate point cloud by Gaussian sampling.
    
    Args:
        n (int) : sample's size.
        center (list of float): center of points cloud.
        scales (float | array of float) : standard deviations.
        orientation (array) : spherical coordinates of the first component given by pca.
    
    Returns:
        Points.
    
    """
    
    def __rotation_matrix(u,theta):
        """Give the rotation matrix relative to a direction and an angle.
        
        Args:
            u (1d numpy array) : 3d vector for rotation direction.
            theta (float) : rotation angle in radians.
            
        Returns:
            (2d numpy array of shape (3,3)) : rotation matrix.
        
        
        """
        P=np.kron(u,u).reshape(3,3)
        Q=np.diag([u[1]],k=2)+np.diag([-u[2],-u[0]],k=1)+np.diag([u[2],u[0]],k=-1)+np.diag([-u[1]],k=-2)
        return P+np.cos(theta)*(np.eye(3)-P)+np.sin(theta)*Q
    
    # Simulation of a gaussian sample whose components are exactly
    # the canonical vectors
    X = scs.norm.rvs(loc=center,scale=scales,size=(n,3))
    
    theta, phi = orientation
    
    # Getting the asked orientation after some rotations
    R=__rotation_matrix([0,0,1],theta)
    v=np.cross(np.dot(R,[1,0,0]),[0,0,1])
    R=np.dot(__rotation_matrix(v,np.pi/2-phi),R)
    
    return Points(np.dot(X,R.transpose()))

def gen_sphere(n=1000,rho=1):
    """Generate random uniform point cloud on a sphere.
    
    Args:
        n (int) : sample's size.
        rho (int or float) : sphere's radius.
        
    Returns:
        Points.
    
    """
    
    #Simulation with spherical coordinates
    thetas=np.arccos(-2*np.random.random_sample(n)+1)  
    phis=2*np.pi*np.random.random_sample(n)
    pts=np.zeros((n,3))
    # theta polar angle
    # phi azimuthal angle
    for theta,phi,i in zip(thetas,phis,np.arange(n)):
        pts[i]=[rho*np.sin(theta)*np.cos(phi),rho*np.sin(theta)*np.sin(phi),rho*np.cos(theta)]
    return Points(pts)

def gen_blobs(**kwargs):
    """Generate isotropic gaussian blobs for clustering.
    
    Args:
        **kwargs : make_blobs keyword agruments in scikitlearn.
        
    Returns:
        Tuple containing
            - Points.
            - labels (array) : point label.
    
    """
    
    pts,labels=make_blobs(**kwargs)
    return (Points(pts),labels)

#def read_csv(file_path):
#    """Generate 3d points with datas inside a file.
#    
#    
#    Args
#        file_path (str) : directory and name of a file.
#    
#    Returns 
#        (Points object) created with file's datas.
#    
#    """
#    data=pd.read_csv(file_path,header=None)
#    pts=data.values
#    return Points(pts)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
