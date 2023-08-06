# -*- coding: utf-8 -*-
"""
User defined functions for LightPipes for Python

"""
import numpy as _np
from .field import Field
from .core import BeamMix

def RowOfFields(Fin,Ffield,Nfields,sep,y=0.0):
    """
    *Inserts an row of fields in the field*
    
    :param Fin: input field
    :type Fin: Field 
    :param Ffield: field to be inserted
    :type Ffield: Field, numpy.ndarray 
    :param Nfields: number of inserted field in x-direction
    :type Nfields: int, float
    :param sep: separation of the inserted fields in the x-direction
    :type sep: int, float
    :param y: position of the row in the y-direction (Default = 0.0)
    :type y: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> #Insert a row of fields or numpy arrays in the input field at y (Default=0.0):    
    >>> F=Begin(size,wavelength,N)
    >>> #Define the field, Ffield, to be inserted:
    >>> Nfield=int(size_field/size*N)
    >>> Ffield=Begin(size_field,wavelength,Nfield)
    >>> Ffield=CircAperture(Ffield,Dlens/2)
    >>> Ffield=Lens(Ffield,f)
    >>> #Insert the Ffield's in the field F:
    >>> F=RowOfFields(F,Ffield,Nfields,sep)
    >>> Ifields=Intensity(F)
    
    .. seealso::
        
        * :ref:`Examples: Multi- holes and slits. <Multi- holes and slits.>`
    
    """
    if (Nfields+1)*sep > Fin.siz:
       print('Field to be inserted does not fit in input field')
       exit(1)
    Fout = Field.copy(Fin)
    Fout.field*=0.0
    isField=False
    if isinstance(Ffield, Field):
        isField=True
        Nfieldx=Ffield.N
        Nfieldy=Ffield.N
    else:
        Nfieldy, Nfieldx = Ffield.shape
    ch=int(Nfieldy/2)
    cw=int(Nfieldx/2)
    N2=int(Fin.N/2)
    for i in range(0,Nfields):
        if (Nfields %2) == 0.0:
            sx=(i+1/2-int(Nfields/2))*sep
        else:
            sx=(i-int(Nfields/2))*sep
        sy=y
        Nx=-int(sx/Fin.siz*Fin.N)
        Ny=int(sy/Fin.siz*Fin.N)
        Nx_field=N2-cw-Nx
        Ny_field=N2-ch-Ny
        if isField:
            Fout.field[Ny_field:Ny_field+Nfieldy, Nx_field:Nx_field+Nfieldx]=Ffield.field
        else:
            Fout.field[Ny_field:Ny_field+Nfieldy, Nx_field:Nx_field+Nfieldx]=Ffield
    return Fout


 
def FieldArray2D(Fin,Ffield,Nfieldsx,Nfieldsy,x_sep,y_sep):
    """
    *Inserts an array of fields in the field*
    
    :param Fin: input field
    :type Fin: Field 
    :param Ffield: field to be inserted
    :type Ffield: Field  
    :param Nfieldsx: number of inserted field in x-direction
    :type Nfieldsx: int, float
    :param Nfieldy: number of inserted field in y-direction
    :type Nfieldy: int, float
    :param x_sep: separation of the inserted fields in the x-direction
    :type x_sep: int, float
    :param y_sep: separation of the inserted fields in the y-direction
    :type y_sep: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:

    >>> #Insert an array of lenses in the field    
    >>> F=Begin(size,wavelength,N)
    >>> #Define the field, Ffield, to be inserted:
    >>> Nfield=int(size_field/size*N)
    >>> Ffield=Begin(size_field,wavelength,Nfield)
    >>> Ffield=CircAperture(Ffield,Dlens/2)
    >>> Ffield=Lens(Ffield,f)
    >>> #Insert the Ffield's in the field F:
    >>> F=FieldArray2D(F,Ffield,Nfields,Nfields,x_sep,y_sep)
    >>> Ifields=Intensity(F)
    
    .. seealso::
        
        * :ref:`Examples: Shack Hartmann sensor <Shack Hartmann sensor.>`
    """

    Fout = Field.copy(Fin)
    F = _np.ndarray((Nfieldsy,),dtype=_np.object)
    F[0]=Ffield
    if (Nfieldsy %2) == 0:
        Nfieldsy2=int(Nfieldsy/2)
        ys=(1/2-Nfieldsy2)*y_sep
    else:
        Nfieldsy2=int((Nfieldsy-1)/2)
        ys=-Nfieldsy2*y_sep        
    F[0]=RowOfFields(Fin,Ffield,Nfieldsx,x_sep,ys)
    for i in range(1,Nfieldsy):
        if (Nfieldsy %2) == 0:
            ys=(i+1/2-Nfieldsy2)*y_sep
        else:
            ys=(i-Nfieldsy2)*y_sep
        F[i]=RowOfFields(Fin,Ffield,Nfieldsx,x_sep,ys)
        F[i]=BeamMix(F[i-1],F[i])
    Fout=F[Nfieldsy-1]
    return Fout
    
def CylindricalLens(Fin,f,x_shift=0.0,y_shift=0.0,angle=0.0):
    Fout = Field.copy(Fin)
    _2pi = 2*_np.pi
    k = _2pi/Fout.lam
    yy, xx = Fout.mgrid_cartesian
    xx -= x_shift
    yy -= y_shift
    if angle!=0.0:
        ang_rad = -1*angle*_np.pi/180.0 #-1 copied from Cpp convention
        cc = _np.cos(ang_rad)
        ss = _np.sin(ang_rad)
        xxr = cc * xx + ss * yy
        yyr = -ss * xx + cc * yy
        yy, xx = yyr, xxr
    fi = -k*(xx**2)/(2*f)
    Fout.field *= _np.exp(1j * fi)
    return Fout
