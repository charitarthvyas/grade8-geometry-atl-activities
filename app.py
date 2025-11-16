
import streamlit as st
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='Grade 8 Geometry - ATL Activities (Visual)', layout='wide')

st.title('Grade 8 Geometry — Interactive ATL Activities (with 2D visuals)')
st.markdown('Three inquiry-based interactive activities to practise **Critical Thinking** in geometry. Simple 2D visuals have been added to help students connect dimensions with shapes.')

tabs = st.tabs(["1. Surface Area Explorer", "2. Compound Volume Designer", "3. Scale Factor Patterns"])

# Helper: draw simple 2D shape diagrams using matplotlib
def draw_cylinder(ax, radius, height):
    # represent as rectangle height and semicircles left/right for clarity
    circle_resolution = 200
    # rectangle coordinates
    rect_x = [0, height, height, 0, 0]
    rect_y = [-radius, -radius, radius, radius, -radius]
    ax.plot(rect_x, rect_y, color='black')
    # semicircles at left (x=0) and right (x=height)
    theta = np.linspace(-np.pi/2, np.pi/2, circle_resolution)
    left_x = 0 + radius * np.cos(theta)
    left_y = radius * np.sin(theta)
    right_x = height + radius * np.cos(np.pi - theta)
    right_y = radius * np.sin(theta)
    ax.plot(left_x, left_y, color='black')
    ax.plot(right_x, right_y, color='black')
    ax.set_aspect('equal', 'box')
    ax.axis('off')
    ax.set_title(f'Cylinder (r={radius}, h={height})', fontsize=10)

def draw_cone(ax, radius, height):
    # triangle base from x=0 to x=height, base centered vertically
    apex_x = 0
    apex_y = 0
    base_left = height
    base_half = radius
    base_y1 = -base_half
    base_y2 = base_half
    ax.plot([apex_x, base_left], [apex_y, base_y1], color='black')
    ax.plot([apex_x, base_left], [apex_y, base_y2], color='black')
    # base line
    ax.plot([base_left, base_left], [base_y1, base_y2], color='black')
    ax.set_aspect('equal', 'box')
    ax.axis('off')
    ax.set_title(f'Cone (r={radius}, h={height})', fontsize=10)

def draw_sphere(ax, radius):
    theta = np.linspace(0, 2*math.pi, 200)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    ax.plot(x, y, color='black')
    ax.set_aspect('equal', 'box')
    ax.axis('off')
    ax.set_title(f'Sphere (r={radius})', fontsize=10)

def draw_hemisphere(ax, radius):
    theta = np.linspace(0, math.pi, 200)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    ax.plot(x, y, color='black')
    # base line
    ax.plot([-radius, radius], [0,0], color='black')
    ax.set_aspect('equal', 'box')
    ax.axis('off')
    ax.set_title(f'Hemisphere (r={radius})', fontsize=10)


# --- Surface Area Explorer ---
with tabs[0]:
    st.header('Surface Area Explorer — Change dimensions and analyse results')
    st.write('Use the sliders to change dimensions of a shape and observe how surface area changes. Visual diagrams are provided to support reasoning.')
    shape = st.selectbox('Choose a 3D shape', ['Cylinder','Cone','Sphere','Hemisphere'])
    col1, col2 = st.columns([1,1])
    if shape == 'Cylinder':
        r = col1.slider('Radius (units)', 1.0, 20.0, 5.0)
        h = col2.slider('Height (units)', 1.0, 40.0, 10.0)
        sa = 2*math.pi*r*(r+h)
        vol = math.pi*r*r*h
        st.write(f'**Surface Area** = 2πr(r + h) = {sa:.2f} sq. units')
        st.write(f'**Volume** = πr²h = {vol:.2f} cu. units')
        fig, ax = plt.subplots(figsize=(4,3))
        draw_cylinder(ax, r, h/2)  # scaled for display
        st.pyplot(fig)
    elif shape == 'Cone':
        r = col1.slider('Radius (units)', 1.0, 20.0, 4.0)
        h = col2.slider('Height (units)', 1.0, 40.0, 8.0)
        l = math.sqrt(r*r + h*h)
        sa = math.pi*r*(r + l)
        vol = (1/3)*math.pi*r*r*h
        st.write(f'**Surface Area** = πr(r + l) where l = √(r² + h²) = {sa:.2f} sq. units')
        st.write(f'**Volume** = (1/3)πr²h = {vol:.2f} cu. units')
        fig, ax = plt.subplots(figsize=(4,3))
        draw_cone(ax, r, h/2)
        st.pyplot(fig)
    elif shape == 'Sphere':
        r = col1.slider('Radius (units)', 1.0, 20.0, 6.0)
        sa = 4*math.pi*r*r
        vol = (4/3)*math.pi*r**3
        st.write(f'**Surface Area** = 4πr² = {sa:.2f} sq. units')
        st.write(f'**Volume** = (4/3)πr³ = {vol:.2f} cu. units')
        fig, ax = plt.subplots(figsize=(4,3))
        draw_sphere(ax, r)
        st.pyplot(fig)
    elif shape == 'Hemisphere':
        r = col1.slider('Radius (units)', 1.0, 20.0, 6.0)
        sa = 3*math.pi*r*r  # including base
        vol = (2/3)*math.pi*r**3
        st.write(f'**Surface Area (including base)** = 3πr² = {sa:.2f} sq. units')
        st.write(f'**Volume** = (2/3)πr³ = {vol:.2f} cu. units')
        fig, ax = plt.subplots(figsize=(4,3))
        draw_hemisphere(ax, r)
        st.pyplot(fig)

    st.markdown('**Generate a small data table** (varying the chosen dimension) to observe pattern:')
    if st.button('Generate table of values'):
        if shape in ['Cylinder','Cone']:
            radii = np.linspace(max(1.0, r-3), r+3, 7)
            heights = np.linspace(max(1.0, h-5), h+5, 7)
            data = []
            for rr in radii:
                for hh in heights:
                    if shape == 'Cylinder':
                        sa_val = 2*math.pi*rr*(rr+hh)
                    else:
                        lval = math.sqrt(rr*rr + hh*hh)
                        sa_val = math.pi*rr*(rr + lval)
                    data.append({'radius': round(rr,2),'height': round(hh,2),'surface_area': round(sa_val,2)})
            df = pd.DataFrame(data)
            st.dataframe(df.head(20))
        else:
            radii = np.linspace(max(1.0, r-3), r+3, 13)
            data = []
            for rr in radii:
                if shape == 'Sphere':
                    sa_val = 4*math.pi*rr*rr
                else:
                    sa_val = 3*math.pi*rr*rr
                data.append({'radius': round(rr,2),'surface_area': round(sa_val,2)})
            df = pd.DataFrame(data)
            st.dataframe(df)

# --- Compound Volume Designer ---
with tabs[1]:
    st.header('Compound Volume Designer — Build and justify a container')
    st.write('Combine basic solids to design a container with a target capacity. The app computes the combined volume and shows simple 2D sketches for each component.')
    target = st.number_input('Target capacity (cubic units)', min_value=1.0, value=100.0)
    st.write('Add up to three components. Choose shape and parameters for each.')
    components = []
    sketches = []
    for i in range(1,4):
        with st.expander(f'Component {i} (optional)'):
            use = st.checkbox(f'Use component {i}', value=(i==1))
            if use:
                shape_c = st.selectbox(f'Shape {i}', ['Cylinder','Rectangular Prism','Cone','Sphere'], key=f'shape{i}')
                if shape_c == 'Cylinder':
                    r = st.number_input(f'Radius {i}', min_value=0.1, value=3.0, key=f'r{i}')
                    h = st.number_input(f'Height {i}', min_value=0.1, value=5.0, key=f'h{i}')
                    vol = math.pi*r*r*h
                    sketches.append(('cylinder', r, h))
                elif shape_c == 'Rectangular Prism':
                    l = st.number_input(f'Length {i}', min_value=0.1, value=5.0, key=f'l{i}')
                    w = st.number_input(f'Width {i}', min_value=0.1, value=4.0, key=f'w{i}')
                    h = st.number_input(f'Height {i}', min_value=0.1, value=3.0, key=f'ph{i}')
                    vol = l*w*h
                    sketches.append(('prism', l, w, h))
                elif shape_c == 'Cone':
                    r = st.number_input(f'Radius {i}', min_value=0.1, value=2.0, key=f'cr{i}')
                    h = st.number_input(f'Height {i}', min_value=0.1, value=6.0, key=f'ch{i}')
                    vol = (1/3)*math.pi*r*r*h
                    sketches.append(('cone', r, h))
                else:
                    r = st.number_input(f'Radius {i}', min_value=0.1, value=2.0, key=f'sr{i}')
                    vol = (4/3)*math.pi*r**3
                    sketches.append(('sphere', r))
                components.append({'component': i, 'shape': shape_c, 'volume': vol})
    total_vol = sum([c['volume'] for c in components])
    st.write(f'Calculated total volume: {total_vol:.2f} cubic units. Target: {target:.2f}')
    if total_vol >= target:
        st.success('Design meets or exceeds target capacity. Provide justification and consider material use.')
    else:
        st.warning('Design does not meet target capacity. Consider resizing or adding components.')

    # show simple sketches
    if sketches:
        cols = st.columns(len(sketches))
        for i, s in enumerate(sketches):
            fig, ax = plt.subplots(figsize=(3,2))
            typ = s[0]
            if typ == 'cylinder':
                draw_cylinder(ax, s[1], s[2]/2)
            elif typ == 'prism':
                # draw rectangle for prism using length and height approx
                l, w, h = s[1], s[2], s[3]
                rect_x = [0, h, h, 0, 0]
                rect_y = [-l/2, -l/2, l/2, l/2, -l/2]
                ax.plot(rect_x, rect_y, color='black')
                ax.set_aspect('equal', 'box')
                ax.axis('off')
                ax.set_title(f'Prism (l={l}, h={h})', fontsize=9)
            elif typ == 'cone':
                draw_cone(ax, s[1], s[2]/2)
            else:
                draw_sphere(ax, s[1])
            cols[i].pyplot(fig)

    # Provide printable summary
    if st.button('Export design summary'):
        summary_lines = ['Compound Container Design Summary\n']
        for c in components:
            summary_lines.append(f"Component {c['component']}: {c['shape']} — volume = {c['volume']:.2f}")
        summary_lines.append(f'Total volume = {total_vol:.2f} (target {target:.2f})')
        st.code('\n'.join(summary_lines))

# --- Scale Factor Patterns ---
with tabs[2]:
    st.header('Scale Factor Patterns — Observe how SA and Volume scale')
    st.write('Pick a base shape and apply a range of scale factors. Observe numeric growth and plot patterns. Simple 2D diagrams illustrate base shape.')
    base_shape = st.selectbox('Base shape', ['Cube','Sphere','Cylinder'])
    base_size = st.slider('Base linear measure (units): e.g., side length or radius', 1.0, 10.0, 3.0)
    scale_min = st.number_input('Minimum scale factor', min_value=0.1, value=0.5)
    scale_max = st.number_input('Maximum scale factor', min_value=0.1, value=2.0)
    steps = st.slider('Number of steps', 3, 20, 8)
    factors = np.linspace(scale_min, scale_max, steps)
    results = []
    for f in factors:
        s = base_size * f
        if base_shape == 'Cube':
            sa = 6*(s**2)
            vol = s**3
        elif base_shape == 'Sphere':
            sa = 4*math.pi*s*s
            vol = (4/3)*math.pi*s**3
        else:
            # cylinder: treat base_size as radius and use a fixed height equal to base_size for visualization
            r = s
            h = base_size * f  # proportional height
            sa = 2*math.pi*r*(r+h)
            vol = math.pi*r*r*h
        results.append({'factor': round(f,3), 'linear': round(s,3), 'surface_area': round(sa,3), 'volume': round(vol,3)})
    df = pd.DataFrame(results)
    st.dataframe(df)

    # show base shape sketch
    fig, ax = plt.subplots(figsize=(3,2))
    if base_shape == 'Cube':
        # draw square for cube representation
        s = base_size
        rect_x = [0, s, s, 0, 0]
        rect_y = [0, 0, s, s, 0]
        ax.plot(rect_x, rect_y, color='black')
        ax.set_title(f'Cube (side={base_size})', fontsize=10)
    elif base_shape == 'Sphere':
        draw_sphere(ax, base_size)
    else:
        draw_cylinder(ax, base_size, base_size/2)
    ax.axis('off')
    ax.set_aspect('equal', 'box')
    st.pyplot(fig)

    # Plotting SA and Volume growth
    fig2, ax2 = plt.subplots()
    ax2.plot(df['factor'], df['surface_area'], marker='o', label='Surface Area')
    ax2.plot(df['factor'], df['volume'], marker='o', label='Volume')
    ax2.set_xlabel('Scale factor')
    ax2.set_ylabel('Value (units)')
    ax2.set_title('Growth of Surface Area and Volume with scale factor')
    ax2.legend()
    st.pyplot(fig2)

    st.markdown('**Teacher prompts:** Ask students to describe how SA and Volume change when linear dimensions are doubled. Invite algebraic explanation.')

st.markdown('---\n**Notes for teachers:** Use these interactive activities and sketches to collect formative evidence of ATL skill development: ask students to submit short justifications, screenshots, and design summaries.')
