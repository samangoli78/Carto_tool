import os,re
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


class Parser_carto:
    def __init__(self,carto=None):
        self.carto=carto
        self.bipolar=None
        self.unipolar=None
        self.vertices=None
        self.triangles=None
    def parse_mesh_file(self):
        vertices = []
        triangles = []
        name=""
        for m in [i for i in [x for x,y in self.carto.files_cat()] if i.endswith(".mesh")]:
            name+=m
        with open(os.path.join(self.carto.path,m), 'r',errors="ignore") as file:
            lines = file.readlines()
            vertices_section = False
            triangles_section = False
            k=0
            for line in lines:
            
                line = line.strip()
                if line.startswith('[VerticesSection]'):
                    vertices_section = True
                    triangles_section = False
                if line.startswith('[TrianglesSection]'):
                    vertices_section = False
                    triangles_section = True
                if line.startswith("[VerticesColorsSection]"):
                    vertices_section = False
                    triangles_section = False
                if vertices_section and '=' in line:
                    parts = line.split('=')
                    coords = parts[1].strip().split()[:3]
                    vertices.append([float(coord) for coord in coords])
                if triangles_section and '=' in line:
                    if k==0: 
                        k=1
                        continue
                    parts = line.split('=')
                    indices = parts[1].strip().split()[:3]
                    triangles.append([int(index) for index in indices])

        return np.array(vertices), np.array(triangles)
        
    def mesh_build(self):
        vertices, triangles = self.parse_mesh_file()
        self.test=triangles
        faces = np.hstack([[3] + list(tri) for tri in triangles])
        return [vertices, faces]
    
    def pars_mesh_file_with_electrode(self,file=None):
        vertices = []
        triangles = []
        unipolar_values = []
        bipolar_values = []
        if not file:
            name=""
            for m in [i for i in [x for x,y in self.carto.files_cat()] if i.endswith(".mesh")]:
                name+=m
            path=os.path.join(self.carto.path,name)
        else:
            path=file
        with open(path, 'r',errors="ignore") as file:
            lines = file.readlines()
            vertices_section = False
            triangles_section = False
            vertices_colors_section = False
            f=0
            f1=0
            for line in lines:
                line = line.strip()
                if line.startswith('[VerticesSection]'):
                    vertices_section = True
                    triangles_section = False
                    vertices_colors_section = False
                if line.startswith('[TrianglesSection]'):
                    vertices_section = False
                    triangles_section = True
                    vertices_colors_section = False
                if line.strip()=="[VerticesColorsSection]":
                    vertices_section = False
                    triangles_section = False
                    vertices_colors_section = True
                if line.strip() == "[VerticesAttributesSection]":
                    vertices_colors_section = False
                if vertices_section and '=' in line:
                    parts = line.split('=')
                    coords = parts[1].strip().split()[:3]
                    vertices.append([float(coord) for coord in coords])
                if triangles_section and '=' in line:
                    if f==0:
                        f=1
                        continue
                    parts = line.split('=')
                    indices = parts[1].strip().split()[:3]
                    triangles.append([int(index) for index in indices])
                if vertices_colors_section and '=' in line:
                    if f1==0:
                        f1=1
                        continue
                    parts = line.split('=')
                    colors = parts[1].strip().split()
                    unipolar_values.append(float(colors[0]))
                    bipolar_values.append(float(colors[1]))
        self.unipolar=np.array(unipolar_values)
        self.bipolar=np.array(bipolar_values)
        self.vertices=np.array(vertices)
        self.triangles=np.array(triangles)
        return np.array(vertices), np.array(triangles), np.array(unipolar_values), np.array(bipolar_values)
    

    

                
            