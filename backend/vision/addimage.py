from google.cloud import vision_v1p3beta1 as gvision
from vision.clients import __get_vision_client

def create_reference_image(
    project_id, location, product_id, gcs_uri
):
    """Create a reference image.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
        gcs_uri: Google Cloud Storage path of the input image.
    """
    client = __get_vision_client()

    return_dict = {}
    status = 200

    try:
        # Get the full path of the product.
        product_path = client.product_path(
            project=project_id, location=location, product=product_id
        )

        # Create a reference image.
        reference_image = gvision.ReferenceImage(uri=gcs_uri)

        # The response is the reference image with `name` populated.
        image = client.create_reference_image(
            parent=product_path,
            reference_image=reference_image
        )

        # Display the reference image information.
        full_resource_name = image.name
        reference_image_id_generated = full_resource_name.split('/')[-1]

        # create a dictionary with image name, image uri, and image id
        return_dict = {
            'Reference image name:' : image.name,
            'Reference image uri:' : image.uri,
            'Reference image id:' : reference_image_id_generated
        }   
        print('Reference image name:', image.name)
        print('Reference image uri:', image.uri)
        print('Reference image id:', reference_image_id_generated)

    except Exception as e:
        # print the error to string
        print('Error: ', str(e))
        status = 500

    return return_dict, status

