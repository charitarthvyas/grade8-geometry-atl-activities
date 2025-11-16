
import streamlit as st
import numpy as np
import math
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title='Grade 8 Geometry - ATL Activities (3D)', layout='wide')

st.title('Grade 8 Geometry — Interactive ATL Activities (3D visuals)')
st.markdown('Three inquiry-based interactive activities to practise **Critical Thinking** in geometry. Fully interactive 3D visuals (Plotly) included: zoom, rotate, and inspect.')

tabs = st.tabs(["1. Surface Area Explorer (3D)", "2. Compound Volume Designer (3D)", "3. Scale Factor Patterns (3D)"])

# --- Helpers to create 3D meshes using parametric surfaces ---
def sphere_mesh(radius=1, u_res=30, v_res=30):
    u = np.linspace(0, 2*np.pi, u_res)
    v = np.linspace(0, np.pi, v_res)
    u, v = np.meshgrid(u, v)
    x = radius * np.cos(u) * np.sin(v)
    y = radius * np.sin(u) * np.sin(v)
    z = radius * np.cos(v)
    return x, y, z

def hemisphere_mesh(radius=1, u_res=30, v_res=15):
    # hemisphere: v from 0 to pi/2
    u = np.linspace(0, 2*np.pi, u_res)
    v = np.linspace(0, np.pi/2, v_res)
    u, v = np.meshgrid(u, v)
    x = radius * np.cos(u) * np.sin(v)
    y = radius * np.sin(u) * np.sin(v)
    z = radius * np.cos(v)
    return x, y, z

def cylinder_mesh(radius=1, height=2, theta_res=50, h_res=10):
    theta = np.linspace(0, 2*np.pi, theta_res)
    h = np.linspace(-height/2, height/2, h_res)
    theta, h = np.meshgrid(theta, h)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = h
    return x, y, z

def cone_mesh(radius=1, height=2, theta_res=50, h_res=20):
    # create cone as surface: for each z from 0 to height, radius scales linearly
    z = np.linspace(0, height, h_res)
    theta = np.linspace(0, 2*np.pi, theta_res)
    z, theta = np.meshgrid(z, theta)
    r = (1 - z/height) * radius
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    zz = z - height/2  # center vertically
    return x, y, zz

def prism_mesh(length=2, width=1, height=1):
    # simple cuboid corners
    x = np.array([0, length, length, 0, 0, length, length, 0])
    y = np.array([0, 0, width, width, 0, 0, width, width])
    z = np.array([0, 0, 0, 0, height, height, height, height])
    return x, y, z

# --- Activity 1: Surface Area Explorer ---
with tabs[0]:
    st.header('Surface Area Explorer — 3D interactive models')
    st.write('Choose a shape, rotate and zoom the 3D model, and change dimensions to observe surface area and volume. Use the table generator to collect data.')
    shape = st.selectbox('Choose a 3D shape', ['Sphere','Hemisphere','Cylinder','Cone'])
    col1, col2 = st.columns([1,1])
    if shape == 'Sphere':
        r = col1.slider('Radius (units)', 0.5, 10.0, 3.0)
        sa = 4*math.pi*r*r
        vol = (4/3)*math.pi*r**3
        st.write(f'**Surface Area** = 4πr² = {sa:.2f} sq. units')
        st.write(f'**Volume** = (4/3)πr³ = {vol:.2f} cu. units')
        x, y, z = sphere_mesh(r, 40, 20)
        fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale='Viridis', showscale=False, opacity=0.9)])
        fig.update_layout(scene=dict(aspectmode='data'), margin=dict(l=0,r=0,t=30,b=0))
        st.plotly_chart(fig, use_container_width=True)
    elif shape == 'Hemisphere':
        r = col1.slider('Radius (units)', 0.5, 10.0, 3.0)
        sa = 3*math.pi*r*r  # including base
        vol = (2/3)*math.pi*r**3
        st.write(f'**Surface Area (including base)** = 3πr² = {sa:.2f} sq. units')
        st.write(f'**Volume** = (2/3)πr³ = {vol:.2f} cu. units')
        x, y, z = hemisphere_mesh(r, 40, 20)
        fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale='Plasma', showscale=False, opacity=0.9)])
        # add base disk for hemisphere
        theta = np.linspace(0, 2*math.pi, 50)
        xx = r * np.cos(theta)
        yy = r * np.sin(theta)
        zz = np.zeros_like(theta) - 0.0
        fig.add_trace(go.Mesh3d(x=xx, y=yy, z=zz, color='lightgrey', opacity=0.5))
        fig.update_layout(scene=dict(aspectmode='data'), margin=dict(l=0,r=0,t=30,b=0))
        st.plotly_chart(fig, use_container_width=True)
    elif shape == 'Cylinder':
        r = col1.slider('Radius (units)', 0.5, 10.0, 2.0)
        h = col2.slider('Height (units)', 0.5, 20.0, 6.0)
        sa = 2*math.pi*r*(r+h)
        vol = math.pi*r*r*h
        st.write(f'**Surface Area** = 2πr(r + h) = {sa:.2f} sq. units')
        st.write(f'**Volume** = πr²h = {vol:.2f} cu. units')
        x, y, z = cylinder_mesh(r, h, 60, 40)
        fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale='Cividis', showscale=False, opacity=0.9)])
        # add top and bottom disks
        theta = np.linspace(0, 2*math.pi, 60)
        xt = r*np.cos(theta)
        yt = r*np.sin(theta)
        zt_top = np.ones_like(theta)*(h/2)
        zt_bot = np.ones_like(theta)*(-h/2)
        fig.add_trace(go.Mesh3d(x=xt, y=yt, z=zt_top, color='lightgrey', opacity=0.5))
        fig.add_trace(go.Mesh3d(x=xt, y=yt, z=zt_bot, color='lightgrey', opacity=0.5))
        fig.update_layout(scene=dict(aspectmode='data'), margin=dict(l=0,r=0,t=30,b=0))
        st.plotly_chart(fig, use_container_width=True)
    else:  # Cone
        r = col1.slider('Radius (units)', 0.5, 10.0, 2.0)
        h = col2.slider('Height (units)', 0.5, 20.0, 6.0)
        l = math.sqrt(r*r + h*h)
        sa = math.pi*r*(r + l)
        vol = (1/3)*math.pi*r*r*h
        st.write(f'**Surface Area** = πr(r + l) where l = √(r² + h²) = {sa:.2f} sq. units')
        st.write(f'**Volume** = (1/3)πr²h = {vol:.2f} cu. units')
        x, y, z = cone_mesh(r, h, 60, 40)
        fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale='Inferno', showscale=False, opacity=0.9)])
        # add base disk
        theta = np.linspace(0, 2*math.pi, 60)
        xx = r*np.cos(theta)
        yy = r*np.sin(theta)
        zz = np.zeros_like(theta) - h/2
        fig.add_trace(go.Mesh3d(x=xx, y=yy, z=zz, color='lightgrey', opacity=0.5))
        fig.update_layout(scene=dict(aspectmode='data'), margin=dict(l=0,r=0,t=30,b=0))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('**Generate a small data table** (varying the chosen dimension) to observe pattern:')
    if st.button('Generate table of values'):
        data = []
        if shape in ['Cylinder','Cone']:
            radii = np.linspace(max(0.5, r-2), r+2, 7)
            heights = np.linspace(max(0.5, h-3), h+3, 7)
            for rr in radii:
                for hh in heights:
                    if shape == 'Cylinder':
                        sa_val = 2*math.pi*rr*(rr+hh)
                    else:
                        lval = math.sqrt(rr*rr + hh*hh)
                        sa_val = math.pi*rr*(rr + lval)
                    data.append({'radius': round(rr,2),'height': round(hh,2),'surface_area': round(sa_val,2)})
        else:
            radii = np.linspace(max(0.5, r-2), r+2, 13)
            for rr in radii:
                if shape == 'Sphere':
                    sa_val = 4*math.pi*rr*rr
                else:
                    sa_val = 3*math.pi*rr*rr
                data.append({'radius': round(rr,2),'surface_area': round(sa_val,2)})
        df = pd.DataFrame(data)
        st.dataframe(df)

# --- Activity 2: Compound Volume Designer (3D) ---
with tabs[1]:
    st.header('Compound Volume Designer — 3D')
    st.write('Combine basic solids to design a container with a target capacity. Rotate and inspect components in 3D; the app computes combined volume.')
    target = st.number_input('Target capacity (cubic units)', min_value=1.0, value=150.0)
    st.write('Add up to three components. Choose shape and parameters for each.')
    components = []
    meshes = []
    for i in range(1,4):
        with st.expander(f'Component {i} (optional)'):
            use = st.checkbox(f'Use component {i}', value=(i==1))
            if use:
                shape_c = st.selectbox(f'Shape {i}', ['Cylinder','Rectangular Prism','Cone','Sphere'], key=f'shape{i}')
                if shape_c == 'Cylinder':
                    r = st.number_input(f'Radius {i}', min_value=0.1, value=3.0, key=f'r{i}')
                    h = st.number_input(f'Height {i}', min_value=0.1, value=5.0, key=f'h{i}')
                    vol = math.pi*r*r*h
                    x,y,z = cylinder_mesh(r,h,40,20)
                    meshes.append((x,y,z, 'cylinder', r, h))
                elif shape_c == 'Rectangular Prism':
                    l = st.number_input(f'Length {i}', min_value=0.1, value=5.0, key=f'l{i}')
                    w = st.number_input(f'Width {i}', min_value=0.1, value=4.0, key=f'w{i}')
                    h = st.number_input(f'Height {i}', min_value=0.1, value=3.0, key=f'ph{i}')
                    vol = l*w*h
                    x,y,z = prism_mesh(l,w,h)
                    meshes.append((x,y,z, 'prism', l, w, h))
                elif shape_c == 'Cone':
                    r = st.number_input(f'Radius {i}', min_value=0.1, value=2.0, key=f'cr{i}')
                    h = st.number_input(f'Height {i}', min_value=0.1, value=6.0, key=f'ch{i}')
                    vol = (1/3)*math.pi*r*r*h
                    x,y,z = cone_mesh(r,h,40,20)
                    meshes.append((x,y,z, 'cone', r, h))
                else:
                    r = st.number_input(f'Radius {i}', min_value=0.1, value=2.0, key=f'sr{i}')
                    vol = (4/3)*math.pi*r**3
                    x,y,z = sphere_mesh(r,30,15)
                    meshes.append((x,y,z, 'sphere', r))
                components.append({'component': i, 'shape': shape_c, 'volume': vol})
    total_vol = sum([c['volume'] for c in components])
    st.write(f'Calculated total volume: {total_vol:.2f} cubic units. Target: {target:.2f}')
    if total_vol >= target:
        st.success('Design meets or exceeds target capacity. Provide justification and consider material use.')
    else:
        st.warning('Design does not meet target capacity. Consider resizing or adding components.')

    # Combine meshes into one 3D figure for inspection
    if meshes:
        fig = go.Figure()
        for idx, m in enumerate(meshes):
            if m[3] == 'prism':
                x, y, z = m[0], m[1], m[2]
                # draw edges of prism as lines
                fig.add_trace(go.Mesh3d(x=x, y=y, z=z, color='lightblue', opacity=0.5))
            else:
                x, y, z = m[0], m[1], m[2]
                fig.add_trace(go.Surface(x=x, y=y, z=z, showscale=False, opacity=0.9))
        fig.update_layout(scene=dict(aspectmode='data'), margin=dict(l=0,r=0,t=30,b=0))
        st.plotly_chart(fig, use_container_width=True)

    if st.button('Export design summary'):
        summary_lines = ['Compound Container Design Summary\n']
        for c in components:
            summary_lines.append(f"Component {c['component']}: {c['shape']} — volume = {c['volume']:.2f}")
        summary_lines.append(f'Total volume = {total_vol:.2f} (target {target:.2f})')
        st.code('\n'.join(summary_lines))

# --- Activity 3: Scale Factor Patterns (3D) ---
with tabs[2]:
    st.header('Scale Factor Patterns — 3D interactive visualization')
    st.write('Choose a base shape, apply scale factors, inspect 3D shapes, and observe numeric growth and plots.')
    base_shape = st.selectbox('Base shape', ['Cube','Sphere','Cylinder'])
    base_size = st.slider('Base linear measure (units): side length or radius', 0.5, 6.0, 2.0)
    scale_min = st.number_input('Minimum scale factor', min_value=0.1, value=0.5)
    scale_max = st.number_input('Maximum scale factor', min_value=0.1, value=2.0)
    steps = st.slider('Number of steps', 3, 20, 8)
    factors = np.linspace(scale_min, scale_max, steps)
    results = []
    figs = []
    for f in factors:
        s = base_size * f
        if base_shape == 'Cube':
            sa = 6*(s**2)
            vol = s**3
            # make simple cube as mesh (use prism_mesh)
            x,y,z = prism_mesh(s,s,s)
            fig = go.Figure(data=[go.Mesh3d(x=x, y=y, z=z, color='orange', opacity=0.6)])
        elif base_shape == 'Sphere':
            sa = 4*math.pi*s*s
            vol = (4/3)*math.pi*s**3
            x,y,z = sphere_mesh(s,30,20)
            fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, showscale=False, opacity=0.8)])
        else:
            r = s
            h = base_size * f  # proportional height
            sa = 2*math.pi*r*(r+h)
            vol = math.pi*r*r*h
            x,y,z = cylinder_mesh(r,h,40,20)
            fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, showscale=False, opacity=0.8)])
        fig.update_layout(scene=dict(aspectmode='data'), margin=dict(l=0,r=0,t=20,b=0), title=f'Scale factor: {f:.2f}')
        figs.append(fig)
        results.append({'factor': round(f,3), 'linear': round(s,3), 'surface_area': round(sa,3), 'volume': round(vol,3)})
    df = pd.DataFrame(results)
    st.dataframe(df)
    # show one interactive 3D example (the middle one)
    mid = len(figs)//2
    st.plotly_chart(figs[mid], use_container_width=True)
    # Plot growth curves (2D)
    import plotly.express as px
    dfm = df.melt(id_vars=['factor','linear'], value_vars=['surface_area','volume'], var_name='measure', value_name='value')
    fig2 = px.line(dfm, x='factor', y='value', color='measure', markers=True, title='Growth of Surface Area and Volume with scale factor')
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('**Teacher prompts:** Ask students to describe how SA and Volume change when linear dimensions are doubled. Invite algebraic explanation and ask students to inspect shapes in 3D.')

st.markdown('---\n**Notes for teachers:** Use these interactive 3D activities for formative evidence: screenshots, short written explanations, and exported design summaries. Consider device capabilities: Plotly 3D is heavier than 2D plotting; prefer desktop/laptop for smooth performance.')
