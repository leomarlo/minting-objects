from google.cloud import vision
from google.protobuf import field_mask_pb2 as field_mask

def create_product(
    project_id, location, product_id, product_display_name, product_category
):
    """Create one product.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
        product_display_name: Display name of the product.
        product_category: Category of the product.
    """
    client = vision.ProductSearchClient()

    # A resource that represents Google Cloud Platform location.
    location_path = f"projects/{project_id}/locations/{location}"

    # Create a product with the product specification in the region.
    # Set product display name and product category.
    product = vision.Product(
        display_name=product_display_name, product_category=product_category
    )

    # The response is the product with the `name` field populated.
    response = client.create_product(
        parent=location_path, product=product, product_id=product_id
    )

    # Display the product information.
    print(f"Product name: {response.name}")




def add_product_to_product_set(project_id, location, product_id, product_set_id):
    """Add a product to a product set.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
        product_set_id: Id of the product set.
    """
    client = vision.ProductSearchClient()

    # Get the full path of the product set.
    product_set_path = client.product_set_path(
        project=project_id, location=location, product_set=product_set_id
    )

    # Get the full path of the product.
    product_path = client.product_path(
        project=project_id, location=location, product=product_id
    )

    # Add the product to the product set.
    client.add_product_to_product_set(name=product_set_path, product=product_path)
    print("Product added to product set.")


def remove_product_from_product_set(project_id, location, product_id, product_set_id):
    """Remove a product from a product set.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
        product_set_id: Id of the product set.
    """
    client = vision.ProductSearchClient()

    # Get the full path of the product set.
    product_set_path = client.product_set_path(
        project=project_id, location=location, product_set=product_set_id
    )

    # Get the full path of the product.
    product_path = client.product_path(
        project=project_id, location=location, product=product_id
    )

    # Remove the product from the product set.
    client.remove_product_from_product_set(name=product_set_path, product=product_path)
    print("Product removed from product set.")

