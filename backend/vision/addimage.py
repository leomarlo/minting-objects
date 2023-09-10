from google.cloud import vision

def create_reference_image(
    project_id, location, product_id, reference_image_id, gcs_uri
):
    """Create a reference image.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
        reference_image_id: Id of the reference image.
        gcs_uri: Google Cloud Storage path of the input image.
    """
    client = vision.ProductSearchClient()

    # Get the full path of the product.
    product_path = client.product_path(
        project=project_id, location=location, product=product_id
    )

    # Create a reference image.
    reference_image = vision.ReferenceImage(uri=gcs_uri)

    # The response is the reference image with `name` populated.
    image = client.create_reference_image(
        parent=product_path,
        reference_image=reference_image,
        reference_image_id=reference_image_id,
    )

    # Display the reference image information.
    print(f"Reference image name: {image.name}")
    print(f"Reference image uri: {image.uri}")

