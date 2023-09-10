from google.cloud import vision_v1p3beta1 as gvision
from vision.clients import __get_vision_client

def create_product_set(project_id, location, product_set_id, product_set_display_name):
    """Create a product set.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_set_id: Id of the product set.
        product_set_display_name: Display name of the product set.
    """
    client = __get_vision_client()

    # A resource that represents Google Cloud Platform location.
    location_path = f"projects/{project_id}/locations/{location}"

    # Create a product set with the product set specification in the region.
    product_set = gvision.ProductSet(display_name=product_set_display_name)

    # The response is the product set with `name` populated.
    response_dict = {}
    status = 200
    try:
        response = client.create_product_set(
            parent=location_path, product_set=product_set, product_set_id=product_set_id
        )
        response_dict = {'Product set name:': response.name}
    except Exception as e:
        # print the error to string
        print('Error: ', str(e))
        status = 500

    return response_dict, status

