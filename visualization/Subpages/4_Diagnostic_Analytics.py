import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import numpy as np
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

# Initialize session state for selected variables if not already initialized
if 'selected_features' not in st.session_state:
    st.session_state['selected_features'] = []
    
# Function to calculate correlation and regression
def calculate_regression(df, feature_1, feature_2):
    # Calculate correlation using numpy
    correlation_value = np.corrcoef(df[feature_1], df[feature_2])[0, 1]
    
    # Perform linear regression using scipy
    slope, intercept, r_value, p_value, std_err = stats.linregress(df[feature_1], df[feature_2])
    
    return correlation_value, r_value**2, p_value  # r_value**2 is R-squared

# Function to perform K-Means clustering and calculate performance metrics
def perform_clustering(df, features, num_clusters):
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    clusters = kmeans.fit_predict(df[features])
    inertia = kmeans.inertia_  # Sum of squared distances to the closest cluster center
    
    if num_clusters > 1:
        silhouette_avg = silhouette_score(df[features], clusters)
    else:
        silhouette_avg = None
    
    return clusters, kmeans, inertia, silhouette_avg

# Function to reduce the dimensions of the data using PCA
def reduce_to_2d(df, features):
    pca = PCA(n_components=2)  # Reduce to 2D
    reduced_data = pca.fit_transform(df[features])
    return reduced_data

# Access data from session state in other subpages
if 'df' in st.session_state and 'raw_df' in st.session_state:
    df = st.session_state['df']
    raw_df = st.session_state['raw_df']
else:
    st.error("Data not loaded. Please go back to the main page to load the data.")

# Doctor Profile and Title
doctor_name = "Dr. Emily Stone"
doctor_image_base64 = st.session_state.get('doctor_image_base64', '')

with st.container():
    r1, r2 = st.columns([2, 1])
    with r1:
        r1.title("Diagnostic Analytics")
    with r2:
        st.markdown(
            f"""
            <div class="doctor-profile" style="display: flex; align-items: center; justify-content: flex-end;">
                <span class="notification-bell" title="Notifications" style="font-size: 15px; margin-right: 5px;">
                    🔔
                </span>
                <h4 style="margin: 0; font-size: 14px; margin-right: 0px;">{doctor_name}</h4>
                <img src="data:image/png;base64,{doctor_image_base64}" alt="Doctor Picture" style="width: 35px; height: auto;">
            </div>
            """, unsafe_allow_html=True
        )

# Instructions
with st.expander("Instructions", icon=":material/info:", expanded=True):
    st.write("""
    This **Diagnostic Analytics** dashboard allows you to explore relationships between different variables in the dataset. 
    Use the provided options to analyze correlations, cluster variables, and uncover diagnostic insights. 
    Follow the prompts below each visualization for a clear understanding of the results.
    """)

if not df.empty:
    # Ensure numeric columns from the dataset are available for initial selection
    numeric_features = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    # Use session state to maintain the feature selection
    if 'selected_variables' not in st.session_state:
        st.session_state['selected_variables'] = numeric_features  # Default to numeric features
    
    st.subheader("Correlation Analysis")
    # Info Expander for explaining the pair plot
    with st.expander("What is Correlation Analysis?", icon=":material/info:"):
        st.write("""
        **Correlation analysis** measures the strength and direction of the linear relationship between two variables. 
        The correlation coefficient (often referred to as "r") ranges from -1 to 1:
        
        - **1**: Perfect positive correlation – as one variable increases, the other increases.
        - **0**: No linear relationship – the variables are independent of each other.
        - **-1**: Perfect negative correlation – as one variable increases, the other decreases.
        
        The **correlation heatmap** visually represents these relationships between selected variables in the dataset. 
        Colors indicate the strength of the correlation:
        
        - **Positive correlations** are shown in shades of green/yellow (closer to +1).
        - **Negative correlations** are shown in shades of blue (closer to -1).
        
        Use this tool to quickly identify strong relationships between features.
        """)

    # UI for variable selection
    selected_variables = st.multiselect(
        "Choose variables to include in correlation heatmap:",
        df.columns.tolist(),
        default=st.session_state['selected_variables'],  # Start with numeric features selected
        key="feature_multiselect"
    )

    # Button to select all features
    if st.button("Select all"):
        st.session_state['selected_variables'] = df.columns.tolist()  # Select all features
        selected_variables = df.columns.tolist()  # Update selected variables

    # Organize layout in two columns: left for insights, right for heatmap
    col1, col2 = st.columns([1, 2])

    if len(selected_variables) > 1:
        # Compute the correlation matrix
        correlation_matrix = df[selected_variables].corr()

        # Visualize the correlation matrix using Plotly
        with col2:
            st.subheader("**Correlation Heatmap**")

            fig = go.Figure(data=go.Heatmap(
                z=correlation_matrix.values,
                x=correlation_matrix.columns,
                y=correlation_matrix.index,
                colorscale='Viridis',  # You can adjust the color scale
                texttemplate="%{z:.2f}",
                hoverongaps=False
            ))

            fig.update_layout(
                title="",
                xaxis_title="Features",
                yaxis_title="Features",
                width=700,
                height=700
            )

            st.plotly_chart(fig, use_container_width=True)

        # Find strong correlations
        strong_positive = []
        strong_negative = []
        very_strong_positive = []
        very_strong_negative = []

        for i in range(len(correlation_matrix.columns)):
            for j in range(i):
                corr_value = correlation_matrix.iloc[i, j]
                if 0.5 <= corr_value < 0.7:
                    strong_positive.append((correlation_matrix.columns[i], correlation_matrix.columns[j], corr_value))
                elif -0.7 < corr_value <= -0.5:
                    strong_negative.append((correlation_matrix.columns[i], correlation_matrix.columns[j], corr_value))
                elif corr_value >= 0.7:
                    very_strong_positive.append((correlation_matrix.columns[i], correlation_matrix.columns[j], corr_value))
                elif corr_value <= -0.7:
                    very_strong_negative.append((correlation_matrix.columns[i], correlation_matrix.columns[j], corr_value))

        # Display correlation insights on the left column
        with col1:
            st.subheader("Correlation Insights")

            # Expander for explaining correlations
            with st.expander("Understanding Correlations", icon=":material/info:"):
                st.write("""
                - **Positive Correlation**: As one variable increases, the other also increases (closer to +1).
                - **Negative Correlation**: As one variable increases, the other decreases (closer to -1).
                - **Strong Correlation**: Between ±0.5 and ±0.7.
                - **Very Strong Correlation**: Above ±0.7.
                """)

            description = ""

            if very_strong_positive or very_strong_negative:
                description += "**Very Strong Correlations (|r| ≥ 0.7):**\n"
                for var1, var2, corr_value in very_strong_positive:
                    description += f"- **{var1}** and **{var2}** have a very strong positive correlation of **{corr_value:.2f}**.\n"
                for var1, var2, corr_value in very_strong_negative:
                    description += f"- **{var1}** and **{var2}** have a very strong negative correlation of **{corr_value:.2f}**.\n"
                description += "\n"

            if strong_positive or strong_negative:
                description += "**Strong Correlations (0.5 ≤ |r| < 0.7):**\n"
                for var1, var2, corr_value in strong_positive:
                    description += f"- **{var1}** and **{var2}** have a strong positive correlation of **{corr_value:.2f}**.\n"
                for var1, var2, corr_value in strong_negative:
                    description += f"- **{var1}** and **{var2}** have a strong negative correlation of **{corr_value:.2f}**.\n"

            if description:
                st.write(description)
            else:
                st.write("No combinations have correlations greater than 0.5 or less than -0.5.")

    # Filter out original numeric columns excluding "has_hypertension"
    @st.cache_resource
    def get_numeric_features(df):
        numeric_features = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        if "has_hypertension" in numeric_features:
            numeric_features.remove("has_hypertension")
        return numeric_features

    # Get numeric features
    numeric_features = get_numeric_features(raw_df)

    # 1. Pair Plot and Feature Comparison Section
    with st.container():
        st.subheader("Pair Plot and Feature Comparison")

        # Info Expander for explaining the pair plot
        with st.expander("What is a Pair Plot & Regression Line?", icon=":material/info:"):
            st.write("""
            A **pair plot** is a grid of scatter plots used to visualize pairwise relationships between different features in the dataset. 
            Each scatter plot shows the relationship between two features, and the diagonal of the grid shows the distribution of each individual feature.
            This allows you to quickly spot patterns and relationships between multiple variables at once.
            
            A **regression line** represents the best fit line through the data points in a scatter plot. It shows the trend or relationship between two variables, allowing you to predict one variable based on the value of another. 
            The closer the data points are to the line, the stronger the relationship. A positive slope indicates a positive relationship, while a negative slope indicates a negative relationship.         
            """)

        # Two columns layout: left for feature selection, right for visualization
        col1, col2 = st.columns([1, 2])

        # Allow the user to select two features for comparison
        with col1:
            st.info("Select two different features.")
            feature_1 = st.selectbox("Select the first feature:", numeric_features, key="feature_1")
            feature_2 = st.selectbox("Select the second feature:", numeric_features, key="feature_2")

            if feature_1 != feature_2:
                # Calculate correlation and regression results using scipy and numpy
                correlation_value, r_squared, p_value = calculate_regression(raw_df, feature_1, feature_2)

                # Generate dynamic text explanation
                significance_text = "statistically significant, meaning the result is unlikely to have occurred by chance" if p_value < 0.05 else "not statistically significant, meaning the result is likely to have occurred by chance"
                
                correlation_strength = (
                    "a strong positive" if correlation_value > 0.7 else
                    "a moderate positive" if 0.3 <= correlation_value <= 0.7 else
                    "a weak positive" if 0 < correlation_value < 0.3 else
                    "a strong negative" if correlation_value < -0.7 else
                    "a moderate negative" if -0.7 <= correlation_value <= -0.3 else
                    "a weak negative" if -0.3 < correlation_value < 0 else "no"
                )

                # Text interpretation for R-squared explanation
                if r_squared > 0:
                    r_squared_explanation = f"This model explains that about **{r_squared*100:.2f}%** of the variation in **{feature_2}** can be predicted by knowing **{feature_1}**."
                else:
                    r_squared_explanation = f"This model shows that changes in **{feature_1}** do not explain much of the variation in **{feature_2}**."

                # Dynamic explanation for the user
                st.write(f"There is {correlation_strength} relationship between **{feature_1}** and **{feature_2}**, meaning that as one variable changes, the other tends to {'increase' if correlation_value > 0 else 'decrease'} (correlation = **{correlation_value:.2f}**).")
                st.write(r_squared_explanation)
                st.write(f"The relationship is considered **{significance_text}** based on a p-value of **{p_value:.4f}**.")
                    
        # Show all pair plots when no specific features are selected
        with col2:
            if feature_1 == feature_2:
                st.subheader("Pair Plot for All Features")

                # Show progress bar while loading the pair plot
                with st.spinner("Loading pair plot... this might take a while for large datasets."):
                    fig = px.scatter_matrix(raw_df[numeric_features])
                    fig.update_layout(width=800, height=800)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                # Scatter plot to visualize the correlation using Plotly
                fig = px.scatter(raw_df, x=feature_1, y=feature_2, trendline="ols", title=f'{feature_1} vs {feature_2}')
                fig.update_layout(xaxis_title=feature_1, yaxis_title=feature_2)
                st.plotly_chart(fig, use_container_width=True)

    # 2. Clustering Section
    df_clustering = df.copy(deep=True)

    with st.container():
        st.subheader("Clustering Analysis")

        # Info Expander for explaining clustering
        with st.expander("What is Clustering?", icon=":material/info:"):
            st.write("""
            Clustering is an unsupervised machine learning technique used to group similar data points together based on their features.
            It helps to identify underlying patterns or groups within your data. In this analysis, we use **K-Means Clustering**, which divides the data into a set number of clusters based on feature similarity.
            We also provide metrics to help you assess the quality of the clustering.
            """)

        st.info("Select features for clustering and the number of clusters.")
            
        # UI for variable selection
        selected_features = st.multiselect(
            "Choose features to include in clustering:",
            df_clustering.columns.tolist(),
            default=st.session_state['selected_features'],  # Start with previously selected features
            key="feature_multiselect_clustering"
        )

        # Button to select all features
        if st.button("Select all features"):
            st.session_state['selected_features'] = df_clustering.columns.tolist()  # Select all features
            selected_features = df_clustering.columns.tolist()  # Update selected features


        # Two columns layout: left for feature selection and number of clusters, right for visualization
        col1, col2 = st.columns([1, 2])

        with col1:
            
            # Select the number of clusters
            num_clusters = st.slider("Select the number of clusters:", min_value=2, max_value=10, value=3)

            # Perform clustering only if features are selected
            if selected_features:
                clusters, kmeans, inertia, silhouette_avg = perform_clustering(df_clustering, selected_features, num_clusters)

                # Add the cluster labels to the dataframe for visualization
                df_clustering['Cluster'] = clusters

                # Provide information about the clustering performance
                st.write(f"Clustering was performed on the selected features, dividing the data into **{num_clusters}** clusters.")
                
                st.write(f"The sum of squared distances to the closest cluster center (inertia) is **{inertia:.2f}**. A lower value means the points are closer to their cluster centers.")
                
                if silhouette_avg is not None:
                    st.write(f"The average silhouette score is **{silhouette_avg:.2f}**. A score closer to 1 means the clusters are well-separated, while a score closer to -1 means they overlap.")

        with col2:
            if selected_features:
                st.subheader(f"Clustering Visualization with {num_clusters} Clusters")

                # Reduce to 2 dimensions using PCA for visualization
                reduced_data = reduce_to_2d(df_clustering, selected_features)
                reduced_df = pd.DataFrame(reduced_data, columns=['PCA 1', 'PCA 2'])
                reduced_df['Cluster'] = clusters  # Add the cluster labels to the reduced dataframe

                # Plot the reduced data with clusters
                fig = px.scatter(reduced_df, x='PCA 1', y='PCA 2', color='Cluster',
                                title=f'Clusters Visualized in 2D with PCA',
                                color_continuous_scale='Viridis')
                fig.update_layout(xaxis_title='PCA 1', yaxis_title='PCA 2')
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.warning("Please select features to perform clustering.")

else:
    st.error("ML-prepared dataset could not be loaded.")


