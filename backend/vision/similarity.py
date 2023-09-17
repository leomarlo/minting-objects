from google.cloud import vision_v1p3beta1 as gvision
from vision.clients import (
    __get_vision_client,
    __get_annotator_client)

def search_products(
        project_id, 
        location, 
        product_set_id, 
        product_category, 
        image_path):
    """Search products.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_set_id: Id of the product set.
        product_category: Category of the product.
        image_path: Path of the image to be searched.
    """

    # product_search_client is needed only for its helper methods.
    product_search_client = __get_vision_client()
    image_annotator_client = __get_annotator_client()

    # Read the image as a stream of bytes.
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    print('we are inside search')
    # Create annotate image request along with product search feature.
    image = gvision.Image(content=content)

    # product search specific parameters
    product_set_path = product_search_client.product_set_path(
        project=project_id, location=location, product_set=product_set_id
    )
    product_search_params = gvision.ProductSearchParams(
        product_set=product_set_path,
        product_categories=[product_category],
        filter="",
    )
    image_context = gvision.ImageContext(product_search_params=product_search_params)

    print('we are now searching')
    # Search products similar to the image.
    max_results = 5 ## TODO: make this a parameter
    response = image_annotator_client.product_search(
        image, image_context=image_context, max_results=max_results
    )
    print('we searched')
    index_time = response.product_search_results.index_time
    print("Product set index time: ")
    print(index_time)

    results = response.product_search_results.results

    print("Search results:")
    # for result in results:
    #     product = result.product

    #     print(f"Score(Confidence): {result.score}")
    #     print(f"Image name: {result.image}")

    #     print(f"Product name: {product.name}")
    #     print("Product display name: {}".format(product.display_name))
    #     print(f"Product description: {product.description}\n")
    #     print(f"Product labels: {product.product_labels}\n")
    
    return [{
        "score": result.score,
        "image": result.image,
        "product_name": result.product.name,
        "product_display_name": result.product.display_name,
        "product_description": result.product.description,
        "product_labels": result.product.product_labels,} 
        for result in results], 200


