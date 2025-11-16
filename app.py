
import streamlit as st
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='Grade 8 Geometry - ATL Activities', layout='wide')

st.title('Grade 8 Geometry — Interactive ATL Activities')
st.markdown('Three inquiry-based interactive activities to practise **Critical Thinking** in geometry.')

tabs = st.tabs(["1. Surface Area Explorer", "2. Compound Volume Designer", "3. Scale Factor Patterns"])

# --- Surface Area Explorer ---
with tabs[0]:
    st.header('Surface Area Explorer — Change dimensions and analyse results')
    st.write('Use the sliders to change dimensions of a shape and observe how surface area changes.')
    shape = st.selectbox('Choose a 3D shape', ['Cylinder','Cone','Sphere','Hemisphere'])
    if shape == 'Cylinder':
        r = st.slider('Radius (units)', 1.0, 20.0, 5.0)
        h = st.slider('Height (units)', 1.0, 40.0, 10.0)
        sa = 2*math.pi*r*(r+h)
        vol = math.pi*r*r*h
        st.write(f'Surface Area = 2πr(r + h) = {sa:.2f} square units')
        st.write(f'Volume = πr²h = {vol:.2f} cubic units')
    elif shape == 'Cone':
        r = st.slider('Radius (units)', 1.0, 20.0, 4.0)
        h = st.slider('Height (units)', 1.0, 40.0, 8.0)
        l = math.sqrt(r*r + h*h)
        sa = math.pi*r*(r + l)
        vol = (1/3)*math.pi*r*r*h
        st.write(f'Surface Area = πr(r + l) where l = sqrt(r² + h²) = {sa:.2f} square units')
        st.write(f'Volume = (1/3)πr²h = {vol:.2f} cubic units')
    elif shape == 'Sphere':
        r = st.slider('Radius (units)', 1.0, 20.0, 6.0)
        sa = 4*math.pi*r*r
        vol = (4/3)*math.pi*r**3
        st.write(f'Surface Area = 4πr² = {sa:.2f} square units')
        st.write(f'Volume = (4/3)πr³ = {vol:.2f} cubic units')
    elif shape == 'Hemisphere':
        r = st.slider('Radius (units)', 1.0, 20.0, 6.0)
        sa = 3*math.pi*r*r  # including base
        vol = (2/3)*math.pi*r**3
        st.write(f'Surface Area (including base) = 3πr² = {sa:.2f} square units')
        st.write(f'Volume = (2/3)πr³ = {vol:.2f} cubic units')

    # interactive table of values
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
    st.write('Combine basic solids to design a container with a target capacity. The app computes the combined volume.')
    target = st.number_input('Target capacity (cubic units)', min_value=1.0, value=100.0)
    st.write('Add up to three components. Choose shape and parameters for each.')
    components = []
    for i in range(1,4):
        with st.expander(f'Component {i} (optional)'):
            use = st.checkbox(f'Use component {i}', value=(i==1))
            if use:
                shape_c = st.selectbox(f'Shape {i}', ['Cylinder','Rectangular Prism','Cone','Sphere'], key=f'shape{i}')
                if shape_c == 'Cylinder':
                    r = st.number_input(f'Radius {i}', min_value=0.1, value=3.0, key=f'r{i}')
                    h = st.number_input(f'Height {i}', min_value=0.1, value=5.0, key=f'h{i}')
                    vol = math.pi*r*r*h
                elif shape_c == 'Rectangular Prism':
                    l = st.number_input(f'Length {i}', min_value=0.1, value=5.0, key=f'l{i}')
                    w = st.number_input(f'Width {i}', min_value=0.1, value=4.0, key=f'w{i}')
                    h = st.number_input(f'Height {i}', min_value=0.1, value=3.0, key=f'ph{i}')
                    vol = l*w*h
                elif shape_c == 'Cone':
                    r = st.number_input(f'Radius {i}', min_value=0.1, value=2.0, key=f'cr{i}')
                    h = st.number_input(f'Height {i}', min_value=0.1, value=6.0, key=f'ch{i}')
                    vol = (1/3)*math.pi*r*r*h
                else:
                    r = st.number_input(f'Radius {i}', min_value=0.1, value=2.0, key=f'sr{i}')
                    vol = (4/3)*math.pi*r**3
                components.append({'component': i, 'shape': shape_c, 'volume': vol})
    total_vol = sum([c['volume'] for c in components])
    st.write(f'Calculated total volume: {total_vol:.2f} cubic units. Target: {target:.2f}')
    if total_vol >= target:
        st.success('Design meets or exceeds target capacity. Provide justification and consider material use.')
    else:
        st.warning('Design does not meet target capacity. Consider resizing or adding components.')

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
    st.write('Pick a base shape and apply a range of scale factors. Observe numeric growth and plot patterns.')
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

    # Plotting
    fig, ax = plt.subplots()
    ax.plot(df['factor'], df['surface_area'], marker='o', label='Surface Area')
    ax.plot(df['factor'], df['volume'], marker='o', label='Volume')
    ax.set_xlabel('Scale factor')
    ax.set_ylabel('Value (units)')
    ax.set_title('Growth of Surface Area and Volume with scale factor')
    ax.legend()
    st.pyplot(fig)

    st.markdown('**Teacher prompts:** Ask students to describe how SA and Volume change when linear dimensions are doubled. Invite algebraic explanation.')

st.markdown('---\n**Notes for teachers:** Use these interactive activities to collect formative evidence of ATL skill development: ask students to submit short justifications, screenshots, and design summaries.')
