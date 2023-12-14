from app.pages.control import (
    default_button_click,
    restart_button_click,
    start_button_click,
    stop_button_click,
    update_button_click,
    update_data_interval,
)


def test_update_button_callback(mocker):
    """Test Update Button."""
    patched_assign_sections = mocker.patch(
        "app.core_api.assign_sections", return_value="button_update"
    )
    output = update_button_click(0, "", "", "", "", "", "", "", "")
    patched_assign_sections.assert_called_once()
    assert output[0] == "button_update"


def test_start_button_callback():
    """Test Start Button."""
    output = start_button_click(0)
    assert output[1] is False


def test_stop_button_callback():
    """Test Stop Button."""
    output = stop_button_click(0)
    assert output[1] is True


def test_restart_button_callback(mocker):
    """Test Reset Button."""
    patched_refresh_sections = mocker.patch("app.core_api.refresh_sections")
    output = restart_button_click(0)
    patched_refresh_sections.assert_called_once()
    assert output[1] == 0


def test_default_button_callback():
    """Test Default Button."""
    output = default_button_click(0)
    assert output[0] == "Dropdowns returned to default values. Click tick to assign."


def test_data_interval_slider_callback():
    """Test Interval Slider."""
    output = update_data_interval(2)
    assert output[0] == 2000
