from scSpatial import io

# def test_select_file():
#     path = io.select_file()
#     assert isinstance(path, str)


def test_open_and_view_image_in_napari() -> None:
    io.open_image("Dapi") # starts a napari window, select Dapi or any other channel


