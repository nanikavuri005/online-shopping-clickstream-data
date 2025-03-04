import streamlit as st
import pandas as pd
from utils.data_processor import process_clickstream_data
from utils.visualizations import (
    plot_shopping_patterns,
    plot_user_clusters,
    plot_session_duration,
    plot_purchase_funnel
)
from utils.segmentation import perform_customer_segmentation
from utils.sample_data import get_sample_data

st.set_page_config(
    page_title="Consumer Behavior Analysis",
    page_icon="🛍️",
    layout="wide"
)

def main():
    st.title("🛍️ Shopping Behavior Analysis Dashboard")
    st.markdown("""
    Analyze consumer behavior through clickstream data visualization and segmentation.
    Upload your CSV file containing clickstream data or use sample data to explore the dashboard.
    """)

    # Data source selection
    data_source = st.radio(
        "Choose Data Source",
        ["Use Sample Data", "Upload Your Data"],
        help="Select sample data to explore the dashboard features or upload your own CSV file"
    )

    df = None
    if data_source == "Use Sample Data":
        sample_df, info = get_sample_data()
        st.info(info)
        df = sample_df
    else:
        uploaded_file = st.file_uploader("Upload Clickstream Data (CSV)", type=['csv'])
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)  # Handle comma-separated files by default
            except Exception as e:
                st.error(f"Error reading CSV file: {str(e)}")
                return

    if df is not None:
        try:
            # Display raw data sample
            st.subheader("📊 Raw Data Sample")
            st.write(df.head())

            # Process data
            processed_df = process_clickstream_data(df)

            # Summary Statistics
            st.header("📊 Summary Statistics")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Users", len(processed_df['user_id'].unique()))
            with col2:
                st.metric("Total Sessions", len(processed_df['session_id'].unique()))
            with col3:
                st.metric("Avg. Session Duration", f"{processed_df['session_duration'].mean():.2f} min")
            with col4:
                st.metric("Conversion Rate", f"{(processed_df['purchased'].mean() * 100):.1f}%")

            # Filters
            st.header("🔍 Data Filters")
            col1, col2 = st.columns(2)
            with col1:
                date_range = st.date_input(
                    "Select Date Range",
                    [processed_df['timestamp'].min(), processed_df['timestamp'].max()]
                )
            with col2:
                user_segment = st.multiselect(
                    "Select User Segments",
                    options=processed_df['segment'].unique().tolist(),
                    default=processed_df['segment'].unique().tolist()
                )

            # Filter data
            filtered_df = processed_df[
                (processed_df['timestamp'].dt.date.between(date_range[0], date_range[1])) &
                (processed_df['segment'].isin(user_segment))
            ]

            # Visualizations
            st.header("📈 Shopping Patterns")
            shopping_patterns_fig = plot_shopping_patterns(filtered_df)
            st.plotly_chart(shopping_patterns_fig, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                st.header("👥 User Clusters")
                clusters_fig = plot_user_clusters(filtered_df)
                st.plotly_chart(clusters_fig, use_container_width=True)

            with col2:
                st.header("⏱️ Session Duration Analysis")
                duration_fig = plot_session_duration(filtered_df)
                st.plotly_chart(duration_fig, use_container_width=True)

            st.header("🔄 Purchase Funnel")
            funnel_fig = plot_purchase_funnel(filtered_df)
            st.plotly_chart(funnel_fig, use_container_width=True)

            # Customer Segmentation
            st.header("🎯 Customer Segmentation Analysis")
            segments = perform_customer_segmentation(filtered_df)
            st.write(segments)

        except Exception as e:
            st.error(f"Error processing data: {str(e)}")
            st.info("Please check if your CSV file contains the required columns: User_ID, Session_ID, Timestamp, Action")

if __name__ == "__main__":
    main()