"""
graphicsHelper.py

Functions to help build graphics data
"""

import igeCore as core
import igeVmath as vmath

_uvs = (0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0)
_tris = (0, 2, 1, 1, 2, 3)
_pivotoffset = (1,-1, 0,-1, -1,-1, 1,0, 0,0, -1,0, 1,1, 0,1, -1,1)


def textFigure(word, fontpath, fontsize,color=(1.0, 1.0, 1.0, 1.0), pivot=4, scale = 1.0):
    '''
    Create Visible text

    Parameters
    ----------
        word : string
            text
        fontpath : string
            font data file path
        fontsize : string
            font size
        color : (float,float,float,float)
            text color
        pivot : int
            center point of polygon
            0       1       2
             +-------+-------+
             |       |       |
            3|      4|      5|
             +-------+-------+
             |       |       |
            6|      7|      8|
             +-------+-------+
    '''

    w,h = core.calcFontPixelSize(word, fontpath, fontsize)
    tex = core.texture(core.unique("text"),w,h, format=core.GL_RED)
    tex.setText(word, fontpath,fontsize)

    gen = core.shaderGenerator()
    gen.setColorTexture(True)
    gen.setBoneCondition(1, 1)
    gen.discardColorMapRGB()

    hw = w/2 * scale
    hh = h/2 * scale
    px = _pivotoffset[pivot*2+0] * hw;
    py = _pivotoffset[pivot*2+1] * hh;

    points = ((-hw+px,hh+py,0.0), (hw+px,hh+py,0.0), (-hw+px,-hh+py,0.0), (hw+px,-hh+py,0.0))

    efig = createMesh(points, _tris, None, _uvs, gen)

    efig.setMaterialParam("mate", "DiffuseColor", color);
    efig.setMaterialParamTexture("mate", "ColorSampler", tex,
                                    wrap_s=core.SAMPLERSTATE_BORDER,wrap_t=core.SAMPLERSTATE_BORDER,
                                    minfilter=core.SAMPLERSTATE_NEAREST, magfilter=core.SAMPLERSTATE_LINEAR)
    efig.setMaterialRenderState("mate", "blend_enable", True)

    return efig


def createSprite(width:float=100, height:float=100, texture=None, uv_left_top:tuple=(0,0), uv_right_bottom:tuple=(1,1), normal=None, pivot=4, shader=None):
    """
    Create Visible Rectangle

	Parameters
	----------
        width : float (optional)
            sprite width
        height: float (optional)
            sprite height
        texture: string (optional)
            texture file name
        uv_left_top: tuple (optional)
            texture uv value of left top cornar
        uv_right_bottom: tuple (optional)
            texture uv value of right bottom cornar
        normal: pyvmath.vec3 (optional)
            specify rectangle's nomal vector
        pivot : int
            center point of polygon
        shader : igeCore.shader
            shader object
	Returns
	-------
        editableFigure
    """
    hw = width/2
    hh = height/2
    px = _pivotoffset[pivot*2+0] * hw;
    py = _pivotoffset[pivot*2+1] * hh;
    points = ((-hw+px,hh+py,0.0), (hw+px,hh+py,0.0), (-hw+px,-hh+py,0.0), (hw+px,-hh+py,0.0))

    if normal is not None:
        newpoints = []
        nom0 = (0, 0, 1)
        mat = vmath.mat33(vmath.quat_rotation(nom0, normal))
        for p in points:
            newpoints.append(mat * p)
        points = newpoints

    # uvs = (uv_left_top[0], uv_right_bottom[1],
    #        uv_right_bottom[0], uv_right_bottom[1],
    #        uv_left_top[0], uv_left_top[1],
    #        uv_right_bottom[1], uv_left_top[1])
    uvs = ( uv_left_top[0], uv_right_bottom[1],
            uv_right_bottom[0], uv_right_bottom[1],
            uv_left_top[0], uv_left_top[1],
            uv_right_bottom[0], uv_left_top[1])

    return createMesh(points, _tris, texture, uvs, shader)


def createMesh(points, tris, texture=None, uvs = None, shader = None, normals = None):
    """
    Create a polygon mesh by specifying vertex coordinates and triangle index

	Parameters
	----------
        points: tuple or list
            list or tuple of points
        tris: tuple or list
            list or tuple of triangle indices
        texture: string (optional)
            file path of texture
        uvs: list or tuple (optional)
        shader : igeCore.shader
            shader object
        normals : list or tuple (optional)
            list or tuple of  vertex normal

	Returns
	-------
        editableFigure
   
    """
    if shader is None:
        shader = core.shaderGenerator()
        if texture != None:
            shader.setColorTexture(True)
        shader.setBoneCondition(1, 1)

    efig = core.editableFigure("sprite")
    efig.addMaterial("mate", shader)
    efig.addMesh("mesh", "mate");

    efig.setVertexElements("mesh", core.ATTRIBUTE_ID_POSITION, points)
    if uvs:
        efig.setVertexElements("mesh", core.ATTRIBUTE_ID_UV0,uvs)

    if  normals:
        efig.setVertexElements("mesh", core.ATTRIBUTE_ID_NORMAL,normals)

    efig.setTriangles("mesh", tris);
    efig.addJoint("joint");
    efig.setMaterialParam("mate", "DiffuseColor", (1.0, 1.0, 1.0, 1.0));
    #efig.setMaterialRenderState("mate", "cull_face_enable", False)

    if texture != None:
        efig.setMaterialParamTexture("mate", "ColorSampler", texture,
                                     wrap_s=core.SAMPLERSTATE_BORDER,wrap_t=core.SAMPLERSTATE_BORDER,
                                     minfilter=core.SAMPLERSTATE_LINEAR, magfilter=core.SAMPLERSTATE_LINEAR)
        efig.setMaterialRenderState("mate", "blend_enable", True)

    return efig
