from google.cloud import vision

def list_product_sets(project_id, location):
    """List all product sets.
    Args:
        project_id: Id of the project.
        location: A compute region name.
    """
    client = vision.ProductSearchClient()
    
    # A resource that represents Google Cloud Platform location.
    location_path = f"projects/{project_id}/locations/{location}"

    # List all the product sets available in the region by calling list_product_sets.
    product_sets = client.list_product_sets(parent=location_path)

    for product_set in product_sets:
        print('Product set name:', product_set.name)
        print('Product set id:', product_set.name.split('/')[-1])
        print('Product set display name:', product_set.display_name)
        print('\n')

# Usage
