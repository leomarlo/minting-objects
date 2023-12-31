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
            'Set_name:': product_set.name,
            'Set_id:' : product_set.name.split('/')[-1],
            'Set_display_name:' : product_set.display_name,
            } for product_set in product_sets]
        
    except Exception as e:
        # print the error to string
        print('Error: ', str(e))
        return_status = 500

    return return_list, return_status


def list_products_in_product_set(project_id, location, product_set_id):
    """ list products in given product set
    """
    client = __get_vision_client()

    return_status = 200
    try:  
        product_set_path = client.product_set_path(project_id, location, product_set_id)
        products = client.list_products_in_product_set(name=product_set_path)
            
        print('we got some product path', product_set_path)
        print('we got some products', [p.name for p in products])
        products_list = []

        for product in products:

            product_id = product.name.split('/')[-1]
            # product_path = client.product_path(
            #         project=project_id, location=location, product=product_id
            #     )
            # reference_images = client.list_reference_images(parent=product_path)
            # image_infos = [{"name": image.name, "uri": image.uri} for image in reference_images]
            # reference_images_count = len(image_infos)


            products_list.append({
                'name': product.name,
                'id' : product_id,
                'displayname' : product.display_name,
                'category' : product.product_category
                # 'Reference images' : image_infos
            })
        # print('product List is', products_list)
    except Exception as e:
        
        # print the error to string
        print('Error: ', str(e))
        return_status = 500
    
    return products_list, return_status



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
                image_infos = [{"name": image.name, "uri": image.uri} for image in reference_images]
                reference_images_count = len(image_infos)

    
                product_dicts.append({
                    'name': product.name,
                    'id' : product_id,
                    'name' : product.display_name,
                    'category' : product.product_category,
                    'nrimages' : reference_images_count,
                    'images' : image_infos
                })


            return_list.append({
                'name': product_set.name,
                'id' : product_set.name.split('/')[-1],
                'displayname' : product_set.display_name,
                'products': product_dicts 
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

