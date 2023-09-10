import os
from google.cloud import vision_v1p3beta1 as vision
from vision.clients import __get_vision_client

def list_product_sets(project_id, location):
    """List all product sets.
    Args:
        project_id: Id of the project.
        location: A compute region name.
    """
    client = __get_vision_client()
    
    # A resource that represents Google Cloud Platform location.
    location_path = f"projects/{project_id}/locations/{location}"

    # List all the product sets available in the region by calling list_product_sets.
    return_list = []
    return_status = 200
    try:
        product_sets = client.list_product_sets(parent=location_path)
        return_list = [{
            'Product set name:': product_set.name,
            'Product set id:' : product_set.name.split('/')[-1],
            'Product set display name:' : product_set.display_name,
            } for product_set in product_sets]
        
    except Exception as e:
        # print the error to string
        print('Error: ', str(e))
        return_status = 500

    return return_list, return_status


def list_products_and_product_sets(project_id, location):
    """List all product sets.
    Args:
        project_id: Id of the project.
        location: A compute region name.
    """
    client = __get_vision_client()
    
    # A resource that represents Google Cloud Platform location.
    location_path = f"projects/{project_id}/locations/{location}"

    # List all the product sets available in the region by calling list_product_sets.
    return_list = []
    return_status = 200
    try:
        product_sets = client.list_product_sets(parent=location_path)
        for product_set in product_sets:
            product_set_path = client.product_set_path(project_id, location, product_set.name.split('/')[-1])
            products = client.list_products_in_product_set(name=product_set_path)
            
            product_dicts = []

            for product in products:

                product_id = product.name.split('/')[-1]
                product_path = client.product_path(
                    project=project_id, location=location, product=product_id
                )
                
                reference_images = client.list_reference_images(parent=product_path)
                reference_images_count = len([image for image in reference_images])

    
                product_dicts.append({
                    'Product name:': product.name,
                    'Product id:' : product_id,
                    'Product display name:' : product.display_name,
                    'Product category:' : product.product_category,
                    'Number of reference images' : reference_images_count
                })


            return_list.append({
                'Product set name:': product_set.name,
                'Product set id:' : product_set.name.split('/')[-1],
                'Product set display name:' : product_set.display_name,
                'Products': product_dicts 
                })
        
    except Exception as e:
        # print the error to string
        print('Error: ', str(e))
        return_status = 500

    return return_list, return_status


def list_reference_images_for_product(project_id, location, product_id):

    client = __get_vision_client()
    return_list = {}
    status = 200
    try:
        product_path = client.product_path(
            project=project_id, location=location, product=product_id
        )
        
        reference_images = client.list_reference_images(parent=product_path)

        # You can transform the list of reference images into a format you prefer for your response
        # Here, we're converting them to a list of their names and URIs
        return_list = [{"name": image.name, "uri": image.uri} for image in reference_images]
    except Exception as e:
        # print the error to string
        print('Error: ', str(e))
        status = 500

    return return_list, status

