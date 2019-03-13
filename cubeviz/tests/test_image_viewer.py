import numpy as np
from glue.core import roi

def test_stats_box_without_subset(cubeviz_layout):
    """
    Tests the stat box underneath the ImageViewer when it is the full spectrum
    """
    cl_viewer = cubeviz_layout.split_views[1]._widget

    cl_viewer._subset = None

    data = cl_viewer._data[0][cl_viewer.current_component_id][cl_viewer._slice_index]

    wave = cl_viewer.cubeviz_layout.get_wavelength(cl_viewer.slice_index)
    data_wave = cl_viewer.cubeviz_unit.convert_value(data, wave=wave)

    assert data_wave is not None

    results = (np.nanmin(data_wave), np.nanmax(data_wave), np.median(data_wave), data_wave.mean(), data_wave.std())
    results_string = r"min={:.4}, max={:.4}, median={:.4}, μ={:.4}, σ={:.4}".format(*results)

    assert results_string == cl_viewer.parent().stats_text.text()

def test_stats_box_with_subset(cubeviz_layout):
    """
    Tests the stat box underneath the ImageViewer when there is an ROI
    """
    cl_viewer = cubeviz_layout.split_views[1]._widget

    # Create a subset (ROI) if there is none
    cl_viewer.apply_roi(roi.CircularROI(xc=6, yc=10, radius=3))

    assert cl_viewer._subset is not None

    mask = cl_viewer._subset.to_mask()[cl_viewer._slice_index]
    data = cl_viewer._data[0][cl_viewer.current_component_id][cl_viewer._slice_index][mask]

    wave = cl_viewer.cubeviz_layout.get_wavelength(cl_viewer.slice_index)
    data_wave = cl_viewer.cubeviz_unit.convert_value(data, wave=wave)

    assert data_wave is not None

    results = (np.nanmin(data_wave), np.nanmax(data_wave), np.median(data_wave), data_wave.mean(), data_wave.std())
    results_string = r"min={:.4}, max={:.4}, median={:.4}, μ={:.4}, σ={:.4}".format(*results)

    assert results_string == cl_viewer.parent().stats_text.text()