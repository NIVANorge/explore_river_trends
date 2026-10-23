# Explore river trends

Streamlit app for exploring **monitored trends in nutrient loads for rivers draining to Oslofjord**.

## Running the Streamlit app

### Option 1: From JupyterHub

 1. Open a terminal on the JupyterHub and `cd` into the `explore_river_trends` directory
    
 2. Run `streamlit run ./app/Home.py`

 3. Open a new browser tab and navigate to https://hub.p.niva.no/hub/user-redirect/proxy/8501/

### Option 2: Docker

 1. Clone the repository and build the Dockerfile with `docker build -t explore_river_trends .`
    
 2. Start the container with `docker run -p 8501:8501 explore_river_trends`

 3. Open a new tab and navigate to http://localhost:8501

 ## Deployed Streamlit App

The app is deployed publicly at https://explore-river-trends.p.niva.no/.
 