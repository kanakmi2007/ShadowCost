"""
fetch_data.py

Downloads the pedestrian street network for a 1km radius around
Times Square, NY using OSMnx, and saves it locally as local_network.graphml.
Includes robust error handling and logging.
"""

import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Constants
TIMES_SQUARE_COORDS = (40.758896, -73.985130)  # Latitude, Longitude for Times Square, NY
SEARCH_RADIUS_METERS = 1000                     # 1 km radius
NETWORK_TYPE = "walk"                           # Pedestrian network
OUTPUT_FILENAME = "local_network.graphml"


def fetch_and_save_network(
    center_point: tuple[float, float] = TIMES_SQUARE_COORDS,
    radius: int = SEARCH_RADIUS_METERS,
    network_type: str = NETWORK_TYPE,
    output_path: str = OUTPUT_FILENAME
) -> Path:
    """
    Downloads the street network from OpenStreetMap via OSMnx and writes to GraphML.

    Parameters:
        center_point: (lat, lon) coordinates of the center point.
        radius: Distance in meters from center_point.
        network_type: OSMnx network type (e.g., 'walk', 'drive', 'bike').
        output_path: Path where GraphML file will be written.

    Returns:
        Path object pointing to the saved file.
    """
    try:
        import osmnx as ox
    except ImportError as e:
        logger.error(
            "OSMnx is not installed. Please install dependencies with:\n"
            "    pip install -r requirements.txt\n"
            f"Original error: {e}"
        )
        raise

    # Configure OSMnx settings if available
    try:
        if hasattr(ox, "settings"):
            ox.settings.use_cache = True
            ox.settings.log_console = False
    except Exception as conf_err:
        logger.warning(f"Could not configure OSMnx settings: {conf_err}")

    logger.info(
        f"Downloading '{network_type}' network within {radius}m of "
        f"Times Square {center_point}..."
    )

    try:
        # Retrieve street network within radius of center_point
        # Handles both OSMnx 1.x and 2.x API structures
        if hasattr(ox, "graph_from_point"):
            graph = ox.graph_from_point(
                center_point,
                dist=radius,
                network_type=network_type
            )
        elif hasattr(ox, "graph") and hasattr(ox.graph, "graph_from_point"):
            graph = ox.graph.graph_from_point(
                center_point,
                dist=radius,
                network_type=network_type
            )
        else:
            raise AttributeError("Unable to locate 'graph_from_point' function in osmnx module.")

    except Exception as dl_err:
        logger.error(f"Failed to download street network from OpenStreetMap: {dl_err}")
        raise RuntimeError(f"Network download error: {dl_err}") from dl_err

    if graph is None or len(graph.nodes) == 0:
        error_msg = "Download completed, but the returned graph contains no nodes or edges."
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.info(
        f"Network downloaded successfully: {len(graph.nodes):,} nodes and {len(graph.edges):,} edges."
    )

    target_file = Path(output_path).resolve()
    logger.info(f"Saving graph to '{target_file}'...")

    try:
        # Ensure parent directory exists
        target_file.parent.mkdir(parents=True, exist_ok=True)

        # Save to GraphML
        if hasattr(ox, "save_graphml"):
            ox.save_graphml(graph, filepath=target_file)
        elif hasattr(ox, "io") and hasattr(ox.io, "save_graphml"):
            ox.io.save_graphml(graph, filepath=target_file)
        else:
            raise AttributeError("Unable to locate 'save_graphml' in osmnx module.")

        logger.info(f"Successfully saved network to {target_file} ({target_file.stat().st_size:,} bytes).")
        return target_file

    except Exception as save_err:
        logger.error(f"Failed to save graph to '{target_file}': {save_err}")
        raise IOError(f"File save error: {save_err}") from save_err


def main():
    try:
        dest = fetch_and_save_network()
        logger.info(f"Process complete. Output file: {dest}")
        sys.exit(0)
    except KeyboardInterrupt:
        logger.warning("\nProcess interrupted by user.")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Process failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
