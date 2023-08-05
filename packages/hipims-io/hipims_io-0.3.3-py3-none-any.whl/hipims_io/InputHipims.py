#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
InputHipims
Generate input files for a hipims flood model
-------------------------------------------------------------------------------
@author: Xiaodong Ming
Created on Tue Mar 31 16:03:57 2020
-------------------------------------------------------------------------------
Assumptions:
- Input DEM is a regular DEM file
- its map unit is meter
- its cellsize is the same in both x and y direction
- its reference position is on the lower left corner of the southwest cell
- All the other grid-based input files must be consistent with the DEM file
To do:
- generate input (including sub-folder mesh and field) and output folders
- generate mesh file (DEM.txt) and field files
- divide model domain into small sections if multiple GPU is used
Structure:
   class InputHipims
       - Initialize an object: __init__
       - set model parameters: 
           set_boundary_condition, set_parameter, set_rainfall, 
           set_gauges_position, set_case_folder, set_runtime, set_device_no,
           add_user_defined_parameter, set_num_of_sections


"""
__author__ = "Xiaodong Ming"
import os
import shutil
import copy
import scipy.signal
import numpy as np
from datetime import datetime
from .Raster import Raster
from .Boundary import Boundary
from .ModelSummary import ModelSummary
from .spatial_analysis import sub2map
from . import indep_functions as indep_f
from . import rainfall_processing as rp
#%% definition of class InputHipims
class InputHipims:
    """To define input files for a HiPIMS flood model case
    Read data, process data, write input files, and save data of a model case.
    Properties (public):
        case_folder: (str) the absolute path of the case folder
        data_folders: (dict) paths for data folders(input, output, mesh, field)
        num_of_sections: (scalar) number of GPUs to run the model
        Boundary: a boundary object of class Boundary to provide boundary cells
            location, ID, type, and source data.
        DEM: a Raster object to provide DEM data [alias: Raster].
        shape: shape of the DEM array
        header: (dict) header of the DEM grid
        Summary: a ModelSummary object to record model information
        Sections: a list of objects of child-class InputHipimsSub
        attributes_default: (dict) default model attribute names and values
        attributes: (dict) model attribute names and values
        times:  (list/numpy array) of four values reprenting model run time in
                seconds: start, end, output interval, backup interval
        device_no: (int) the gpu device id(s) to run model
    Properties (Private):
        _valid_cell_subs: (tuple, int numpy) two numpy array indicating rows
            and cols of valid cells on the DEM array and sorted based on the
            valid_cell_id, starting from the bottom-left valid cell towards
            right and up on the DEM array.
        _outline_cell_subs: (tuple, int numpy) two numpy array indicating rows
            and cols of outline cells on the DEM array and sorted based on the
            valid_cell_id from small to large
    Methods (public):
        set_parameter: set grid-based parameters
        set_boundary_condition: set boundary condition with a boundary list
        set_rainfall: set rainfall mask and sources
        set_gauges_position: set X-Y coordinates of monitoring  gauges
        write_input_files: write all input files or a specific file
        write_grid_files: write grid-based data files
        write_boundary_conditions: write boundary sources, if flow time series
            is given, it will be converted to velocities in x and y directions
        write_gauges_position: write coordinates of monitoring gauges
        write_halo_file: write overlayed cell ID for multiple GPU cases
    Methods(protected):
        _get_cell_subs:
        __divide_grid: split model domain:
        _get_boundary_id_code_array:
        _get_vector_value:
        _write_grid_files:
        _initialize_summary_obj:
        (Private only for base class)
        __write_boundary_conditions:
        __write_gauge_pos:
        __copy_to_all_sections:
    Classes:
        InputHipimsSub: child class of InputHiPIMS, provide information
            of each sub-domain
        Boundary: provide information of boundary conditions
        ModelSummary: record basic information of an object of InputHiPIMS
    """
#%%****************************************************************************
#***************************initialize an object*******************************
    # default parameters
    attributes_default = {'h0':0, 'hU0x':0, 'hU0y':0,
                          'precipitation':0,
                          'precipitation_mask':0,
                          'precipitation_source':np.array([[0, 0], [1, 0]]),
                          'manning':0.035,
                          'sewer_sink':0,
                          'cumulative_depth':0, 'hydraulic_conductivity':0,
                          'capillary_head':0, 'water_content_diff':0,
                          'gauges_pos':np.array([[0, 0]])}
    grid_files = ['z', 'h', 'hU', 'precipitation_mask',
                  'manning', 'sewer_sink', 'precipitation',
                  'cumulative_depth', 'hydraulic_conductivity',
                  'capillary_head', 'water_content_diff']
    def __init__(self, dem_data, num_of_sections=1, case_folder=None):
        """
        dem_data: (Raster object) or (str) provides file name of the DEM data
        """
        self.birthday = datetime.now()
        if type(dem_data) is str:
            self.DEM = Raster(dem_data) # create Raster object
        elif type(dem_data) is Raster:
            self.DEM = dem_data
        self.Raster = self.DEM
        self.shape = self.DEM.shape
        self.header = self.DEM.header
        if case_folder is None:
            case_folder = os.getcwd()
        self.case_folder = case_folder
        self.num_of_sections = num_of_sections
        self.attributes = InputHipims.attributes_default.copy()        
        _ = self.set_runtime()
        # get row and col index of all cells on DEM grid
        self._get_cell_subs()  # add _valid_cell_subs and _outline_cell_subs
        # divide model domain to several sections if it is not a sub section
        # each section contains a "HiPIMS_IO_class.InputHipimsSub" object
        if isinstance(self, InputHipimsSub):
            pass
        else:
            self.__divide_grid()
        self.set_case_folder() # set data_folders
        self.set_device_no() # set the device number
        self.set_boundary_condition(outline_boundary='fall')
        self._initialize_summary_obj()# initialize a Model Summary object
        
    def __str__(self):
        """
        To show object summary information when it is called in console
        """
        self.Summary.display()
        time_str = self.birthday.strftime('%Y-%m-%d %H:%M:%S')
        return  self.__class__.__name__+' object created on '+ time_str
#    __repr__ = __str__
#%%****************************************************************************
#************************Setup the object**************************************
    def set_boundary_condition(self, boundary_list=None,
                               outline_boundary='fall'):
        """To create a Boundary object for boundary conditions
        The object contains
              outline_boundary, a dataframe of boundary type, extent, source
              data, code, ect..., and a boundary subscrpits
              tuple (cell_subs).For multi-GPU case, a boundary subscrpits tuple
              (cell_subs_l) based on sub-grids will be created for each section
        outline_boundary: (str) 'open'|'rigid', default outline boundary is
            open and both h and hU are set as zero
        boundary_list: (list of dicts), each dict contain keys (polyPoints,
            type, h, hU) to define a IO boundary's position, type, and
            Input-Output (IO) sources timeseries. Keys including:
            1.polyPoints is a numpy array giving X(1st col) and Y(2nd col)
                coordinates of points to define the position of a boundary.
                An empty polyPoints means outline boundary.
            2.type: 'open'(flow out flatly), 'rigid'(no outlet),
                    'fall'(water flow out like a fall)
            3.h: a two-col numpy array. The 1st col is time(s). The 2nd col is
                water depth(m)
            4.hU: a two-col numpy array. The 1st col is time(s). The 2nd col is
                discharge(m3/s) or a three-col numpy array, the 2nd col and the
                3rd col are velocities(m/s) in x and y direction, respectively.
        cell_subs: (list of tuple) subsripts of cells for each boundary
        cell_id: (list of vector) valid id of cells for each boundary
        """
        # initialize a Boundary object
        if boundary_list is None and hasattr(self, 'Boundary'):
            boundary_list = self.Boundary.boundary_list
        bound_obj = Boundary(boundary_list, outline_boundary)
        valid_subs = self._valid_cell_subs
        outline_subs = self._outline_cell_subs
        if not isinstance(self, InputHipimsSub):
            dem_header = self.header
        # add the subsripts and id of boundary cells on the domain grid
            bound_obj._fetch_boundary_cells(valid_subs,
                                            outline_subs, dem_header)
        self.Boundary = bound_obj
        if hasattr(self, 'Sections'):
            bound_obj._divide_domain(self)       
        if hasattr(self, 'Summary'):
            summary_dict = bound_obj.get_summary()
            for key, value in summary_dict.items():
                self.Summary.add_items(key, value)

    def set_parameter(self, parameter_name, parameter_value):
        """ Set grid-based parameters
        parameter_name: (str) including: h0, hU0x, hU0y, manning,
            precipitation_mask, sewer_sink, cumulative_depth,
            hydraulic_conductivity, capillary_head, water_content_diff
        parameter_value: (scalar)|(numpy array) with the same size of DEM. All
            parameter values are given to the global grid and can be divided
            to local grids in writing process if multiple sections are defined.
        """
        if parameter_name not in InputHipims.attributes_default.keys():
            raise ValueError('Parameter is not recognized: '+parameter_name)
        if type(parameter_value) is np.ndarray:
            if parameter_value.shape != self.shape:
                raise ValueError('The array of the parameter '
                                 'value should have the same '
                                 'shape with the DEM array')
        elif np.isscalar(parameter_value) is False:
            raise ValueError('The parameter value must be either '
                             'a scalar or an numpy array')
        self.attributes[parameter_name] = parameter_value
        # renew summary information
        self.Summary.add_param_infor(parameter_name, parameter_value)

    def set_rainfall(self, rain_mask=None, rain_source=None):
        """ Set rainfall mask and rainfall source
        rain_mask: numpy int array withe the same size of DEM, each mask
                 value indicates one rainfall source 
                 or a Raster object or a string of mask filename
        rain_source: numpy array the 1st column is time in seconds, 2nd to
             the end columns are rainfall rates in m/s. The number of columns
             in rainfall_source should be equal to the number of mask values
             plus one (the time column)
        """
        # set rain mask
        if rain_mask is None: # use default or pre-defined value
            rain_mask = self.attributes['precipitation_mask']
            rain_mask = np.array(rain_mask).astype('int32')
        elif type(rain_mask) is Raster:
            rain_mask = _generate_mask_for_DEM(rain_mask, self.DEM)
            self.attributes['precipitation_mask'] = rain_mask
        else: # numpy array or scalar
            rain_mask = np.array(rain_mask).astype('int32')
            if rain_mask.size > 1 & rain_mask.shape != self.shape:
                raise ValueError('The shape of rainfall_mask array '
                             'is not consistent with DEM')
            else:
                self.attributes['precipitation_mask'] = rain_mask
        self.Summary.add_param_infor('precipitation_mask', rain_mask)
        # set rain source
        _ = rp._check_rainfall_rate_values(rain_source, times_in_1st_col=True)
        if rain_source is not None:
            self.attributes['precipitation_source'] = rain_source
            rain_mask_unique = np.unique(rain_mask).flatten()
            rain_mask_unique = rain_mask_unique.astype('int32')
            rain_source_valid = np.c_[rain_source[:,0],
                                      rain_source[:,rain_mask_unique+1]]
            self.Summary.add_param_infor('precipitation_source', 
                                         rain_source_valid)

    def set_gauges_position(self, gauges_pos=None):
        """Set coordinates of monitoring gauges
        """
        if gauges_pos is None:
            gauges_pos = self.attributes['gauges_pos']
        if type(gauges_pos) is list:
            gauges_pos = np.array(gauges_pos)
        if gauges_pos.shape[1] != 2:
            raise ValueError('The gauges_pos arraymust have two columns')
        self.attributes['gauges_pos'] = gauges_pos
        self.Summary.add_param_infor('gauges_pos', gauges_pos)
        # for multi_GPU, divide gauges based on the extent of each section
        if self.num_of_sections > 1:
            pos_X = gauges_pos[:,0]
            pos_Y = gauges_pos[:,1]
            for obj_section in self.Sections:
                extent = obj_section.DEM.extent
                ind_x = np.logical_and(pos_X >= extent[0], pos_X <= extent[1])
                ind_y = np.logical_and(pos_Y >= extent[2], pos_Y <= extent[3])
                ind = np.where(np.logical_and(ind_x, ind_y))
                ind = ind[0]
                obj_section.attributes['gauges_pos'] = gauges_pos[ind,:]
                obj_section.attributes['gauges_ind'] = ind

    def set_case_folder(self, new_folder=None, make_dir=False):
        """ Initialize, renew, or create case and data folders
        new_folder: (str) renew case and data folder if it is given
        make_dir: True|False create folders if it is True
        """
        # to change case_folder
        if new_folder is None:
            new_folder = self.case_folder
        self.case_folder = new_folder
        self.data_folders = _create_io_folders(self.case_folder,
                                               make_dir)
        # for multiple GPUs
        if hasattr(self, 'Sections'):
            for obj in self.Sections:
                sub_case_folder = new_folder+'/'+str(obj.section_id)
                obj.set_case_folder(sub_case_folder)                        
        if hasattr(self, 'Summary'):
            self.Summary.set_param('Case folder', self.case_folder)

    def set_runtime(self, runtime=None):
        """set runtime of the model
        runtime: a list of four values representing start, end, output interval
        and backup interval respectively
        """
        if runtime is None:
            runtime = [0, 3600, 3600, 3600]
        runtime = np.array(runtime)
        self.times = runtime
        runtime_str = ('{0}-start, {1}-end, {2}-output interval, '
                       '{3}-backup interval')
        runtime_str = runtime_str.format(*runtime)
        if hasattr(self, 'Summary'):
            self.Summary.add_items('Runtime(s)', runtime_str)
        return runtime_str

    def set_device_no(self, device_no=None):
        """set device no of the model
        device_no: int or a list of int corresponding to the number of sections 
        """
        if device_no is None:
            device_no = np.arange(self.num_of_sections)
        device_no = np.array(device_no)
        self.device_no = device_no

    def add_user_defined_parameter(self, param_name, param_value):
        """ Add a grid-based user-defined parameter to the model
        param_name: (str) name the parameter and the input file name as well
        param_value: (scalar) or (numpy arary) with the same size of DEM array
        """
        if param_name not in InputHipims.grid_files:
            InputHipims.grid_files.append(param_name)
        self.attributes[param_name] = param_value
        print(param_name+ 'is added to the InputHipims object')
        self.Summary.add_param_infor(param_name, param_value)
    
    def set_num_of_sections(self, num_of_sections):
        """ set the number of divided sections to run a case
        can transfer single-gpu to multi-gpu and the opposite way
        """
#        obj_new = copy.deepcopy(self)
        self.num_of_sections = num_of_sections
        self.set_device_no()
        if num_of_sections==1: # to single GPU
            if hasattr(self, 'Sections'):
                del self.Sections
        else: # to multiple GPU
            self.__divide_grid()
            outline_boundary = self.Boundary.outline_boundary
            self.set_boundary_condition(outline_boundary=outline_boundary)
            self.set_gauges_position()
            self.Boundary._divide_domain(self)
        self.set_case_folder(self.case_folder)
        self.birthday = datetime.now()
        self.Summary.set_param('Number of Sections', str(num_of_sections))
        time_str = self.birthday.strftime('%Y-%m-%d %H:%M:%S')
        self.Summary.set_param('Birthday', time_str)
        

    def decomposite_domain(self, num_of_sections):
        """ divide a single-gpu case into a multi-gpu case
        """
        obj_mg = copy.deepcopy(self)
        obj_mg.num_of_sections = num_of_sections
        obj_mg.set_device_no()
        obj_mg.__divide_grid()
        obj_mg.set_case_folder() # set data_folders
        outline_boundary = obj_mg.Boundary.outline_boundary
        obj_mg.set_boundary_condition(outline_boundary=outline_boundary)
        obj_mg.set_gauges_position()
        obj_mg.Boundary._divide_domain(obj_mg)
        obj_mg.birthday = datetime.now()
        return obj_mg

#%%****************************************************************************
#************************Write input files*************************************
    def write_input_files(self, file_tag=None):
        """ Write input files
        To classify the input files and call functions needed to write each
            input files
        file_tag: str or list of str including
                  ['z', 'h', 'hU', 'manning', 'sewer_sink',
                        'cumulative_depth', 'hydraulic_conductivity',
                        'capillary_head', 'water_content_diff',
                        'precipitation_mask', 'precipitation_source',
                        'boundary_condition', 'gauges_pos']
        """
        self._make_data_dirs()
        grid_files = InputHipims.grid_files
        if file_tag is None or file_tag == 'all': # write all files
            file_tag_list = ['z', 'h', 'hU', 'precipitation',
                             'manning', 'sewer_sink',
                             'cumulative_depth', 'hydraulic_conductivity',
                             'capillary_head', 'water_content_diff',
                             'precipitation_mask', 'precipitation_source',
                             'boundary_condition', 'gauges_pos']
            if self.num_of_sections > 1:
                self.write_halo_file()
            self.write_mesh_file()
            self.write_runtime_file()
            self.write_device_file()
        elif type(file_tag) is str:
            file_tag_list = [file_tag]
        elif type(file_tag) is list:
            file_tag_list = file_tag
        else:
            print(file_tag_list)
            raise ValueError(('file_tag should be a string or a list of string'
                             'from the above list'))
        for one_file in file_tag_list:
            if one_file in grid_files: # grid-based files
                self.write_grid_files(one_file)
            elif one_file == 'boundary_condition':
                self.write_boundary_conditions()
            elif one_file == 'precipitation_source':
                self.write_rainfall_source()
            elif one_file == 'gauges_pos':
                self.write_gauges_position()
            else:
                raise ValueError(one_file+' is not recognized')

    def write_grid_files(self, file_tag, is_single_gpu=False):
        """Write grid-based files
        Public version for both single and multiple GPUs
        file_tag: the pure name of a grid-based file
        """
        self._make_data_dirs()
        grid_files = InputHipims.grid_files
        if file_tag not in grid_files:
            raise ValueError(file_tag+' is not a grid-based file')
        if is_single_gpu or self.num_of_sections == 1:
            # write as single GPU even the num of sections is more than one
            self._write_grid_files(file_tag, is_multi_gpu=False)
        else:
            self._write_grid_files(file_tag, is_multi_gpu=True)
        self.Summary.write_readme(self.case_folder+'/readme.txt')
        print(file_tag+' created')

    def write_boundary_conditions(self):
        """ Write boundary condtion files
        if there are multiple domains, write in the first folder
            and copy to others
        """
        self._make_data_dirs()
        if self.num_of_sections > 1:  # multiple-GPU
            field_dir = self.Sections[0].data_folders['field']
            file_names_list = self.__write_boundary_conditions(field_dir)
            self.__copy_to_all_sections(file_names_list)
        else:  # single-GPU
            field_dir = self.data_folders['field']
            self.__write_boundary_conditions(field_dir)
        self.Summary.write_readme(self.case_folder+'/readme.txt')
        print('boundary condition files created')

    def write_rainfall_source(self):
        """Write rainfall source data
        rainfall mask can be written by function write_grid_files
        """
        self._make_data_dirs()
        rain_source = self.attributes['precipitation_source']
        case_folder = self.case_folder
        num_of_sections = self.num_of_sections
        indep_f.write_rain_source(rain_source, case_folder, num_of_sections)
        self.Summary.write_readme(self.case_folder+'/readme.txt')

    def write_gauges_position(self, gauges_pos=None):
        """ Write the gauges position file
        Public version for both single and multiple GPUs
        """
        self._make_data_dirs()
        if gauges_pos is not None:
            self.set_gauges_position(np.array(gauges_pos))
        if self.num_of_sections > 1:  # multiple-GPU
            for obj_section in self.Sections:
                field_dir = obj_section.data_folders['field']
                obj_section.__write_gauge_ind(field_dir)
                obj_section.__write_gauge_pos(field_dir)
        else:  # single-GPU
            field_dir = self.data_folders['field']
            self.__write_gauge_pos(field_dir)
        self.Summary.write_readme(self.case_folder+'/readme.txt')
        print('gauges_pos.dat created')

    def write_halo_file(self):
        """ Write overlayed cell IDs
        """
        num_section = self.num_of_sections
        case_folder = self.case_folder
        if not case_folder.endswith('/'):
            case_folder = case_folder+'/'
        file_name = case_folder+'halo.dat'
        with open(file_name, 'w') as file2write:
            file2write.write("No. of Domains\n")
            file2write.write("%d\n" % num_section)
            for obj_section in self.Sections:
                file2write.write("#%d\n" % obj_section.section_id)
                overlayed_id = obj_section.overlayed_id
                for key in ['bottom_low', 'bottom_high',
                            'top_high', 'top_low']:
                    if key in overlayed_id.keys():
                        line_ids = overlayed_id[key]
                        line_ids = np.reshape(line_ids, (1, line_ids.size))
                        np.savetxt(file2write,
                                   line_ids, fmt='%d', delimiter=' ')
                    else:
                        file2write.write(' \n')
        print('halo.dat created')

    def write_mesh_file(self, is_single_gpu=False):
        """ Write mesh file DEM.txt, compatoble for both single and multiple
        GPU model
        """
        self._make_data_dirs()
        if is_single_gpu is True or self.num_of_sections == 1:
            file_name = self.data_folders['mesh']+'DEM.txt'
            self.DEM.write_asc(file_name)
        else:
            for obj_section in self.Sections:
                file_name = obj_section.data_folders['mesh']+'DEM.txt'
                obj_section.DEM.write_asc(file_name)
        self.Summary.write_readme(self.case_folder+'/readme.txt')
#        print('DEM.txt created')
    
    def write_runtime_file(self, time_values=None):
        """ write times_setup.dat file
        """
        if time_values is None:
            time_values = self.times
        indep_f.write_times_setup(self.case_folder, self.num_of_sections,
                                  time_values)
        self.Summary.write_readme(self.case_folder+'/readme.txt')
    
    def write_device_file(self, device_no=None):
        """Create device_setup.dat for choosing GPU number to run the model
        """
        if device_no is None:
            device_no = self.device_no
        indep_f.write_device_setup(self.case_folder, self.num_of_sections,
                                   device_no)

    def save_object(self, file_name):
        """ Save object as a pickle file
        """
        indep_f.save_object(self, file_name, compression=True)

#%%****************************************************************************
#******************************* Visualization ********************************
    def domain_show(self, figname=None, dpi=None, **kwargs):
        """Show domain map of the object
        """
        obj_dem = copy.deepcopy(self.DEM)
        if hasattr(self, 'Sections'):
            for obj_sub in self.Sections:
                overlayed_subs = obj_sub.overlayed_cell_subs_global
                obj_dem.array[overlayed_subs] = np.nan            
        fig, ax = obj_dem.mapshow(**kwargs)
        cell_subs = self.Boundary.cell_subs
        legends = []
        num = 0
        for cell_sub in cell_subs:
            rows = cell_sub[0]
            cols = cell_sub[1]
            X, Y = sub2map(rows, cols, self.DEM.header)
            ax.plot(X, Y, '.')
            legends.append('Boundary '+str(num))
            num = num+1
        legends[0] = 'Outline boundary'
        ax.legend(legends, edgecolor=None, facecolor=None, loc='best',
                  fontsize='x-small')
        if figname is not None:
            fig.savefig(figname, dpi=dpi)
        return fig, ax
    
    def plot_rainfall_map(self, figname=None, method='sum', **kw):
        """plot rainfall map within model domain
        """
        rain_source = self.attributes['precipitation_source']
        rain_mask = self.attributes['precipitation_mask']
        rain_mask = self.DEM.array*0+rain_mask
        rain_mask_obj = Raster(array=rain_mask, header=self.header)
        rain_map_obj = rp.get_spatial_map(rain_source, rain_mask_obj, figname,
                                          method, **kw)
        return rain_map_obj

    def plot_rainfall_curve(self, start_date=None, method='mean', **kw):
        """ Plot time series of average rainfall rate inside the model domain
        start_date: a datetime object to give the initial date and time of rain
        method: 'mean'|'max','min','mean'method to calculate gridded rainfall 
        over the model domain
        """
        rain_source = self.attributes['precipitation_source']
        rain_mask = self.attributes['precipitation_mask']
        rain_mask = np.array(rain_mask)
        rain_mask = self.DEM.array*0+rain_mask
        plot_data = rp.get_time_series(rain_source, rain_mask, start_date, 
                                    method=method)
        rp.plot_time_series(plot_data, method=method, **kw)
        return plot_data

#%%****************************************************************************
#*************************** Protected methods ********************************
    def _get_cell_subs(self, dem_array=None):
        """ To get valid_cell_subs and outline_cell_subs for the object
        To get the subscripts of each valid cell on grid
        Input arguments are for sub Hipims objects
        _valid_cell_subs
        _outline_cell_subs
        """
        if dem_array is None:
            dem_array = self.DEM.array
        valid_id, outline_id = _get_cell_id_array(dem_array)
        subs = np.where(~np.isnan(valid_id))
        id_vector = valid_id[subs]
        # sort the subscripts according to cell id values
        sorted_vectors = np.c_[id_vector, subs[0], subs[1]]
        sorted_vectors = sorted_vectors[sorted_vectors[:, 0].argsort()]
        self._valid_cell_subs = (sorted_vectors[:, 1].astype('int32'),
                                 sorted_vectors[:, 2].astype('int32'))
        subs = np.where(outline_id == 0) # outline boundary cell
        outline_id_vect = outline_id[subs]
        sorted_array = np.c_[outline_id_vect, subs[0], subs[1]]
        self._outline_cell_subs = (sorted_array[:, 1].astype('int32'),
                                   sorted_array[:, 2].astype('int32'))
    def __divide_grid(self):
        """
        Divide DEM grid to sub grids
        Create objects based on sub-class InputHipimsSub
        """
        if isinstance(self, InputHipimsSub):
            return 0  # do not divide InputHipimsSub objects, return a number
        else:
            if self.num_of_sections == 1:
                return 1 # do not divide if num_of_sections is 1
        num_of_sections = self.num_of_sections
        dem_header = self.header
        # subscripts of the split row [0, 1,...] from bottom to top
        split_rows = _get_split_rows(self.DEM.array, num_of_sections)
        array_local, header_local = \
            _split_array_by_rows(self.DEM.array, dem_header, split_rows)
        # to receive InputHipimsSub objects for sections
        Sections = []
        section_sequence = np.arange(num_of_sections)
        header_global = dem_header
        for i in section_sequence:  # from bottom to top
            case_folder = self.case_folder+'/'+str(i)
            # create a sub object of InputHipims
            sub_hipims = InputHipimsSub(array_local[i], header_local[i],
                                        case_folder, num_of_sections)
            # get valid_cell_subs on the global grid
            valid_cell_subs = sub_hipims._valid_cell_subs
            valid_subs_global = \
                 _cell_subs_convertor(valid_cell_subs, header_global,
                                      header_local[i], to_global=True)
            sub_hipims.valid_subs_global = valid_subs_global
            # record section sequence number
#            sub_hipims.section_id = i
            #get overlayed_id (top two rows and bottom two rows)
            top_h = np.where(valid_cell_subs[0] == 0)
            top_l = np.where(valid_cell_subs[0] == 1)
            bottom_h = np.where(
                valid_cell_subs[0] == valid_cell_subs[0].max()-1)
            bottom_l = np.where(valid_cell_subs[0] == valid_cell_subs[0].max())
            if i == 0: # the bottom section
                overlayed_id = {'top_high':top_h[0], 'top_low':top_l[0]}
            elif i == self.num_of_sections-1: # the top section
                overlayed_id = {'bottom_low':bottom_l[0],
                                'bottom_high':bottom_h[0]}
            else:
                overlayed_id = {'top_high':top_h[0], 'top_low':top_l[0],
                                'bottom_high':bottom_h[0],
                                'bottom_low':bottom_l[0]}
            sub_hipims.overlayed_id = overlayed_id
            all_ids = list(overlayed_id.values())
            all_ids = np.concatenate(all_ids).ravel()
            all_ids.sort()
            overlayed_cell_subs_global = (valid_subs_global[0][all_ids],
                                          valid_subs_global[1][all_ids])
            sub_hipims.overlayed_cell_subs_global = overlayed_cell_subs_global
            Sections.append(sub_hipims)
        # reset global var section_id of InputHipimsSub
        InputHipimsSub.section_id = 0
        self.Sections = Sections
        self._initialize_summary_obj()# get a Model Summary object

    # only for global object
    def _get_vector_value(self, attribute_name, is_multi_gpu=True,
                          add_initial_water=True):
        """ Generate a single vector for values in each grid cell sorted based
        on cell IDs
        attribute_name: attribute names based on a grid
        Return:
            output_vector: a vector of values in global valid grid cells
                            or a list of vectors for each sub domain
        """
        # get grid value
        dem_shape = self.shape
        grid_values = np.zeros(dem_shape)
        if add_initial_water:
            add_value = 0.0001
        else:
            add_value = 0

        def add_water_on_io_cells(bound_obj, grid_values, source_key,
                                  add_value):
            """ add a small water depth/velocity to IO boundary cells
            """
            for ind_num in np.arange(bound_obj.num_of_bound):
                bound_source = bound_obj.data_table[source_key][ind_num]
                if bound_source is not None:
                    source_value = np.unique(bound_source[:, 1:])
                    # zero boundary conditions
                    if not (source_value.size == 1 and source_value[0] == 0):
                        cell_subs = bound_obj.cell_subs[ind_num]
                        grid_values[cell_subs] = add_value
            return grid_values
        # set grid value for the entire domain
        if attribute_name == 'z':
            grid_values = self.DEM.array
        elif attribute_name == 'h':
            grid_values = grid_values+self.attributes['h0']
            # traversal each boundary to add initial water
            grid_values = add_water_on_io_cells(self.Boundary, grid_values,
                                                'hSources', add_value)
        elif attribute_name == 'hU':
            grid_values0 = grid_values+self.attributes['hU0x']
            grid_values1 = grid_values+self.attributes['hU0y']
            grid_values1 = add_water_on_io_cells(self.Boundary, grid_values1,
                                                 'hUSources', add_value)
            grid_values = [grid_values0, grid_values1]
        else:
            grid_values = grid_values+self.attributes[attribute_name]

        def grid_to_vect(grid_values, cell_subs):
            """ Convert grid values to 1 or 2 col vector values
            """
            if type(grid_values) is list:
                vector_value0 = grid_values[0][cell_subs]
                vector_value1 = grid_values[1][cell_subs]
                vector_value = np.c_[vector_value0, vector_value1]
            else:
                vector_value = grid_values[cell_subs]
            return vector_value
        #
        if is_multi_gpu: # generate vector value for multiple GPU
            output_vector = []
            for obj_section in self.Sections:
                cell_subs = obj_section.valid_subs_global
                vector_value = grid_to_vect(grid_values, cell_subs)
                output_vector.append(vector_value)
        else:
            output_vector = grid_to_vect(grid_values, self._valid_cell_subs)
        return output_vector

    def _get_boundary_id_code_array(self, file_tag='z'):
        """
        To generate a 4-col array of boundary cell id (0) and code (1~3)
        """
        bound_obj = self.Boundary
        output_array_list = []
        for ind_num in np.arange(bound_obj.num_of_bound):
            if file_tag == 'h':
                bound_code = bound_obj.data_table.h_code[ind_num]
            elif file_tag == 'hU':
                bound_code = bound_obj.data_table.hU_code[ind_num]
            else:
                bound_code = np.array([[2, 0, 0]]) # shape (1, 3)
            if bound_code.ndim < 2:
                bound_code = np.reshape(bound_code, (1, bound_code.size))
            cell_id = bound_obj.cell_id[ind_num]
            if cell_id.size > 0:
                bound_code_array = np.repeat(bound_code, cell_id.size, axis=0)
                id_code_array = np.c_[cell_id, bound_code_array]
                output_array_list.append(id_code_array)
        # add overlayed cells with [4, 0, 0]
        # if it is a sub section object, there should be attributes:
        # overlayed_id, and section_id
        if hasattr(self, 'overlayed_id'):
            cell_id = list(self.overlayed_id.values())
            cell_id = np.concatenate(cell_id, axis=0)
            bound_code = np.array([[4, 0, 0]]) # shape (1, 3)
            bound_code_array = np.repeat(bound_code, cell_id.size, axis=0)
            id_code_array = np.c_[cell_id, bound_code_array]
            output_array_list.append(id_code_array)
        output_array = np.concatenate(output_array_list, axis=0)
        # when unique the output array according to cell id
        # keep the last occurrence rather than the default first occurrence
        output_array = np.flipud(output_array) # make the IO boundaries first
        _, ind = np.unique(output_array[:, 0], return_index=True)
        output_array = output_array[ind]
        return output_array

    def _initialize_summary_obj(self):
        """ Initialize the model summary object
        """
        summary_obj = ModelSummary(self)
        self.Summary = summary_obj

    def _write_grid_files(self, file_tag, is_multi_gpu=True):
        """ Write input files consistent with the DEM grid
        Private function called by public function write_grid_files
        file_name: includes ['h','hU','precipitation_mask',
                             'manning','sewer_sink',
                             'cumulative_depth', 'hydraulic_conductivity',
                             'capillary_head', 'water_content_diff']
        """
        if is_multi_gpu is True:  # write for multi-GPU, use child object
            vector_value_list = self._get_vector_value(file_tag, is_multi_gpu)
            for obj_section in self.Sections:
                vector_value = vector_value_list[obj_section.section_id]
                cell_id = np.arange(vector_value.shape[0])
                cells_vect = np.c_[cell_id, vector_value]
                file_name = obj_section.data_folders['field']+file_tag+'.dat'
                if file_tag == 'precipitation_mask':
                    bounds_vect = None
                else:
                    bounds_vect = \
                        obj_section._get_boundary_id_code_array(file_tag)
                _write_two_arrays(file_name, cells_vect, bounds_vect)
        else:  # single GPU, use global object
            file_name = self.data_folders['field']+file_tag+'.dat'
            vector_value = self._get_vector_value(file_tag, is_multi_gpu=False)
            cell_id = np.arange(vector_value.shape[0])
            cells_vect = np.c_[cell_id, vector_value]
            if file_tag == 'precipitation_mask':
                bounds_vect = None
            else:
                bounds_vect = self._get_boundary_id_code_array(file_tag)
            _write_two_arrays(file_name, cells_vect, bounds_vect)
        return None

    def _make_data_dirs(self):
        """ Create folders in current device
        """
        if hasattr(self, 'Sections'):
            for obj_section in self.Sections:
                _create_io_folders(obj_section.case_folder, make_dir=True)
        else:
            _create_io_folders(self.case_folder, make_dir=True)
#------------------------------------------------------------------------------
#*************** Private methods only for the parent class ********************
#------------------------------------------------------------------------------
    def __write_boundary_conditions(self, field_dir, file_tag='both'):
        """ Write boundary condition source files,if hU is given as flow
        timeseries, convert flow to hUx and hUy.
        Private function to call by public function write_boundary_conditions
        file_tag: 'h', 'hU', 'both'
        h_BC_[N].dat, hU_BC_[N].dat
        if hU is given as flow timeseries, convert flow to hUx and hUy
        """
        obj_boundary = self.Boundary
        file_names_list = []
        fmt_h = ['%g', '%g']
        fmt_hu = ['%g', '%g', '%g']
        # write h_BC_[N].dat
        if file_tag in ['both', 'h']:
            h_sources = obj_boundary.data_table['hSources']
            ind_num = 0
            for i in np.arange(obj_boundary.num_of_bound):
                h_source = h_sources[i]
                if h_source is not None:
                    file_name = field_dir+'h_BC_'+str(ind_num)+'.dat'
                    np.savetxt(file_name, h_source, fmt=fmt_h, delimiter=' ')
                    ind_num = ind_num+1
                    file_names_list.append(file_name)
        # write hU_BC_[N].dat
        if file_tag in ['both', 'hU']:
            hU_sources = obj_boundary.data_table['hUSources']
            ind_num = 0
            for i in np.arange(obj_boundary.num_of_bound):
                hU_source = hU_sources[i]
                cell_subs = obj_boundary.cell_subs[i]
                if hU_source is not None:
                    file_name = field_dir+'hU_BC_'+str(ind_num)+'.dat'
                    if hU_source.shape[1] == 2:
                        # flow is given rather than speed
                        boundary_slope = np.polyfit(cell_subs[0],
                                                    cell_subs[1], 1)
                        theta = np.arctan(boundary_slope[0])
                        boundary_length = cell_subs[0].size* \
                                          self.DEM.header['cellsize']
                        hUx = hU_source[:, 1]*np.cos(theta)/boundary_length
                        hUy = hU_source[:, 1]*np.sin(theta)/boundary_length
                        hU_source = np.c_[hU_source[:, 0], hUx, hUy]
                        print('Flow series on boundary '+str(i)+
                              ' is converted to velocities')
                        print('Theta = '+'{:.3f}'.format(theta/np.pi)+'*pi')
                    np.savetxt(file_name, hU_source, fmt=fmt_hu, delimiter=' ')
                    ind_num = ind_num+1
                    file_names_list.append(file_name)
        return file_names_list

    def __write_gauge_pos(self, file_folder):
        """write monitoring gauges
        gauges_pos.dat
        file_folder: folder to write file
        gauges_pos: 2-col numpy array of X and Y coordinates
        """
        gauges_pos = self.attributes['gauges_pos']
        file_name = file_folder+'gauges_pos.dat'
        fmt = ['%g %g']
        fmt = '\n'.join(fmt*gauges_pos.shape[0])
        gauges_pos_str = fmt % tuple(gauges_pos.ravel())
        with open(file_name, 'w') as file2write:
            file2write.write(gauges_pos_str)
        return file_name

    def __write_gauge_ind(self, file_folder):
        """write monitoring gauges index for mult-GPU sections
        gauges_ind.dat
        file_folder: folder to write file
        gauges_ind: 1-col numpy array of index values
        """
        gauges_ind = self.attributes['gauges_ind']
        file_name = file_folder+'gauges_ind.dat'
        fmt = ['%g']
        fmt = '\n'.join(fmt*gauges_ind.shape[0])
        gauges_ind_str = fmt % tuple(gauges_ind.ravel())
        with open(file_name, 'w') as file2write:
            file2write.write(gauges_ind_str)
        return file_name

    def __copy_to_all_sections(self, file_names):
        """ Copy files that are the same in each sections
        file_names: (str) files written in the first seciton [0]
        boundary source files: h_BC_[N].dat, hU_BC_[N].dat
        rainfall source files: precipitation_source_all.dat
        gauges position file: gauges_pos.dat
        """
        if type(file_names) is not list:
            file_names = [file_names]
        for i in np.arange(1, self.num_of_sections):
            field_dir = self.Sections[i].data_folders['field']
            for file in file_names:
                shutil.copy2(file, field_dir)

#%%****************************************************************************
#************************sub-class definition**********************************
class InputHipimsSub(InputHipims):
    """object for each section, child class of InputHipims
    Attributes:
        sectionNO: the serial number of each section
        _valid_cell_subs: (tuple, int) two numpy array indicating rows and cols
        of valid cells on the local grid
        valid_cell_subsOnGlobal: (tuple, int) two numpy array indicating rows
        and cols of valid cells on the global grid
        shared_cells_id: 2-row shared Cells id on a local grid
        case_folder: input folder of each section
        _outline_cell_subs: (tuple, int) two numpy array indicating rows and 
        cols of valid cells on a local grid
    """
    section_id = 0
    def __init__(self, dem_array, header, case_folder, num_of_sections):
        self.section_id = InputHipimsSub.section_id
        InputHipimsSub.section_id = self.section_id+1
        dem_data = Raster(array=dem_array, header=header)
        super().__init__(dem_data, num_of_sections, case_folder)

#%%****************************************************************************
#********************************Static method*********************************
def _cell_subs_convertor(input_cell_subs, header_global,
                         header_local, to_global=True):
    """
    Convert global cell subs to divided local cell subs or the otherwise
    and return output_cell_subs, only rows need to be changed
    input_cell_subs : (tuple) input rows and cols of a grid
    header_global : head information of the global grid
    header_local : head information of the local grid
    to_global : logical values, True (local to global) or
                                False(global to local)
    Return:
        output_cell_subs: (tuple) output rows and cols of a grid
    """
    # X and Y coordinates of the centre of the first cell
    y00_centre_global = header_global['yllcorner']+\
                         (header_global['nrows']+0.5)*header_global['cellsize']
    y00_centre_local = header_local['yllcorner']+\
                        (header_local['nrows']+0.5)*header_local['cellsize']
    row_gap = (y00_centre_global-y00_centre_local)/header_local['cellsize']
    row_gap = round(row_gap)
    rows = input_cell_subs[0]
    cols = input_cell_subs[1]
    if to_global:
        rows = rows+row_gap
        # remove subs out of range of the global DEM
        ind = np.logical_and(rows >= 0, rows < header_global['nrows'])
    else:
        rows = rows-row_gap
        # remove subs out of range of the global DEM
        ind = np.logical_and(rows >= 0, rows < header_local['nrows'])
    rows = rows.astype(cols.dtype)
    rows = rows[ind]
    cols = cols[ind]
    output_cell_subs = (rows, cols)
    return output_cell_subs

def _write_two_arrays(file_name, id_values, bound_id_code=None):
    """Write two arrays: cell_id-value pairs and bound_id-bound_code pairs
    Inputs:
        file_name :  the full file name including path
        id_values: valid cell ID - value pair
        bound_id_code: boundary cell ID - codes pair. If bound_id_code is not
            given, then the second part of the file won't be written (only
            the case for precipitatin_mask.dat)
    """
    if not file_name.endswith('.dat'):
        file_name = file_name+'.dat'
    if id_values.shape[1] == 3:
        fmt = ['%d %g %g']
    elif id_values.shape[1] == 2:
        fmt = ['%d %g']
    else:
        raise ValueError('Please check the shape of the 1st array: id_values')
    fmt = '\n'.join(fmt*id_values.shape[0])
    id_values_str = fmt % tuple(id_values.ravel())
    if bound_id_code is not None:
        fmt = ['%-12d %2d %2d %2d']
        fmt = '\n'.join(fmt*bound_id_code.shape[0])
        bound_id_code_str = fmt % tuple(bound_id_code.ravel())
    with open(file_name, 'w') as file2write:
        file2write.write("$Element Number\n")
        file2write.write("%d\n" % id_values.shape[0])
        file2write.write("$Element_id  Value\n")
        file2write.write(id_values_str)
        if bound_id_code is not None:
            file2write.write("\n$Boundary Numbers\n")
            file2write.write("%d\n" % bound_id_code.shape[0])
            file2write.write("$Element_id  Value\n")
            file2write.write(bound_id_code_str)

def _get_cell_id_array(dem_array):
    """ to generate two arrays with the same size of dem_array:
    1. valid_id: to store valid cell id values (sequence number )
        starting from 0, from bottom, left to right, top
    2. outline_id: to store valid cell id on the boundary cells
    valid_id, outline_id = __get_cell_id_array(dem_array)
    """
    # convert DEM to a two-value array: NaNs and Ones
    # and flip up and down
    dem_array_flip = np.flipud(dem_array*0+1)
    # Return the cumulative sum of array elements over a given axis
    # treating NaNs) as zero.
    nancumsum_vector = np.nancumsum(dem_array_flip)
    # sequence number of valid cells: 0 to number of cells-1
    valid_id = nancumsum_vector-1
    # reshape as an array with the same size of DEM
    valid_id = np.reshape(valid_id, np.shape(dem_array_flip))
    # set NaN cells as NaNs
    valid_id[np.isnan(dem_array_flip)] = np.nan
    valid_id = np.flipud(valid_id)
    # find the outline boundary cells
    array_for_outline = dem_array*0
    array_for_outline[np.isnan(dem_array)] = -1
    h_hv = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    # Convolve two array_for_outline arrays
    ind_array = scipy.signal.convolve2d(array_for_outline, h_hv, mode='same')
    ind_array[ind_array < 0] = np.nan
    ind_array[0, :] = np.nan
    ind_array[-1, :] = np.nan
    ind_array[:, 0] = np.nan
    ind_array[:, -1] = np.nan
    # extract the outline cells by a combination
    ind_array = np.isnan(ind_array) & ~np.isnan(dem_array)
    # boundary cells with valid cell id are extracted
    outline_id = dem_array*0-2 # default inner cells value:-2
    outline_id[ind_array] = 0 # outline cells:0
    return valid_id, outline_id

def _get_split_rows(input_array, num_of_sections):
    """ Split array by the number of valid cells (not NaNs) on each rows
    input_array : an array with some NaNs
    num_of_sections : (int) number of sections that the array to be splited
    return split_rows : a list of row subscripts to split the array
    Split from bottom to top
    """
    valid_cells = ~np.isnan(input_array)
    # valid_cells_count by rows
    valid_cells_count = np.sum(valid_cells, axis=1)
    valid_cells_count = np.cumsum(valid_cells_count)
    split_rows = []  # subscripts of the split row [0, 1,...]
    total_valid_cells = valid_cells_count[-1]
    for i in np.arange(num_of_sections-1): 
        num_section_cells = total_valid_cells*(i+1)/num_of_sections
        split_row = np.sum(valid_cells_count<=num_section_cells)-1
        split_rows.append(split_row)
    # sort from bottom to top
    split_rows.sort(reverse=True)
    return split_rows

def _split_array_by_rows(input_array, header, split_rows, overlayed_rows=2):
    """ Clip an array into small ones according to the seperating rows
    input_array : the DEM array
    header : the DEM header
    split_rows : a list of row subscripts to split the array
    Split from bottom to top
    Return array_local, header_local: lists to store local DEM array and header
    """
    header_global = header
    end_row = header_global['nrows']-1
    overlayed_rows = 1
    array_local = []
    header_local = []
    section_sequence = np.arange(len(split_rows)+1)
    for i in section_sequence:  # from bottom to top
        section_id = i
        if section_id == section_sequence.max(): # the top section
            start_row = 0
        else:
            start_row = split_rows[i]-overlayed_rows
        if section_id == 0: # the bottom section
            end_row = header_global['nrows']-1
        else:
            end_row = split_rows[i-1]+overlayed_rows-1
        sub_array = input_array[start_row:end_row+1, :]
        array_local.append(sub_array)
        sub_header = header_global.copy()
        sub_header['nrows'] = sub_array.shape[0]
        sub_yllcorner = (header_global['yllcorner']+
                         (header_global['nrows']-1-end_row)*
                         header_global['cellsize'])
        sub_header['yllcorner'] = sub_yllcorner
        header_local.append(sub_header)
    return array_local, header_local

def _create_io_folders(case_folder, make_dir=False):
    """ create Input-Output path for a Hipims case
        (compatible for single/multi-GPU)
    Return:
      dir_input, dir_output, dir_mesh, dir_field
    """
    folder_name = case_folder
    if not folder_name.endswith('/'):
        folder_name = folder_name+'/'
    dir_input = folder_name+'input/'
    dir_output = folder_name+'output/'
    if not os.path.exists(dir_output) and make_dir:
        os.makedirs(dir_output)
    if not os.path.exists(dir_input) and make_dir:
        os.makedirs(dir_input)
    dir_mesh = dir_input+'mesh/'
    if not os.path.exists(dir_mesh) and make_dir:
        os.makedirs(dir_mesh)
    dir_field = dir_input+'field/'
    if not os.path.exists(dir_field) and make_dir:
        os.makedirs(dir_field)
    data_folders = {'input':dir_input, 'output':dir_output,
                    'mesh':dir_mesh, 'field':dir_field}
    return data_folders

def _generate_mask_for_DEM(mask_origin, dem_data):
    """Interpolate orginal mask file to the dem data
    the interpolating method is nearest
    """
    if type(mask_origin) is str:
        mask_obj = Raster(mask_origin)
    elif type(mask_origin) is Raster:
        mask_obj = mask_origin
    else:
        raise ValueError('mask_origin must be either a filename ',
                         'string or a Raster object')
    if type(dem_data) is str:
        dem_obj = Raster(dem_data)
    elif type(dem_data) is Raster:
        dem_obj = dem_data
    else:
        raise ValueError('mask_origin must be either a filename ',
                         'string or a Raster object')
    mask_on_dem = dem_obj.grid_interpolate(mask_obj)
    mask_on_dem = mask_on_dem.astype('int32')
    return mask_on_dem

def copy_input_obj(obj_in):
    """Copy the an object of class InputHipims
    """
    
    dem_data = Raster(array=obj_in.Raster.array, 
                             header=obj_in.Raster.header)
    num_of_sections = obj_in.num_of_sections
    case_folder = obj_in.case_folder
    # initialize a new object
    obj_copy = InputHipims(dem_data=dem_data, num_of_sections=num_of_sections,
                           case_folder=case_folder)
    attr_dict = copy.deepcopy(obj_in.__dict__)
    if 'Raster' in attr_dict.keys():
        del attr_dict['Raster']
    del attr_dict['Boundary']
    del attr_dict['Summary']
    if num_of_sections > 1:
        del attr_dict['Sections']
    # set object attributes
    for key in attr_dict.keys():
        obj_copy.__dict__[key] = copy.deepcopy(attr_dict[key])
    # set boundary conditions
    boundary_list = obj_in.Boundary.boundary_list
    outline_boundary = obj_in.Boundary.outline_boundary
    obj_copy.set_boundary_condition(boundary_list, outline_boundary)
    # copy summary
    summary_infor = obj_in.Summary.information_dict
    infor_keys = list(summary_infor.keys())
    iloc = 0
    for i in range(len(infor_keys)):
        if infor_keys[i] == 'gauges_pos':
            iloc = i
    infor_keys = infor_keys[iloc+1:]
    for key in infor_keys:
        obj_copy.Summary.add_items(key, summary_infor[key])
    return obj_copy

def main():
    print('Class to setup input data')

if __name__=='__main__':
    main()