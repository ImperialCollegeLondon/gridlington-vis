from contextvars import copy_context

from dash._callback_context import context_value  # type: ignore
from dash._utils import AttributeDict  # type: ignore


def test_control_view_callback(mocker):
    """Test for Control View callback function and buttons."""
    from app.pages.control import update_button_click

    def run_callback():
        context_value.set(
            AttributeDict(
                **{"triggered_inputs": [{"prop_id": f"{button_id}.n_clicks"}]}
            )
        )
        return update_button_click(
            buttons[0],
            buttons[1],
            buttons[2],
            buttons[3],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        )

    """Test Update Button."""
    buttons = [1, None, None, None]
    button_id = "button_update"

    ctx = copy_context()
    patched_assign_sections = mocker.patch(
        "app.core_api.assign_sections", return_value=button_id
    )
    output = ctx.run(run_callback)
    patched_assign_sections.assert_called_once()
    assert output[0] == button_id

    """Test Start Button."""
    buttons = [None, 1, None, None]
    button_id = "button_start"

    ctx = copy_context()
    output = ctx.run(run_callback)
    assert output[0] == "Clicked Start Button!"

    """Test Stop Button."""
    buttons = [None, None, 1, None]
    button_id = "button_stop"

    ctx = copy_context()
    output = ctx.run(run_callback)
    assert output[0] == "Clicked Stop Button!"

    """Test Restart Button."""
    buttons = [None, None, None, 1]
    button_id = "button_restart"

    ctx = copy_context()
    patched_refresh_sections = mocker.patch("app.core_api.refresh_sections")
    output = ctx.run(run_callback)
    patched_refresh_sections.assert_called_once()
    assert output[0] == "Clicked Restart Button!"


def test_default_button_callback():
    """Test Default Button."""
    from app.pages.control import default_button_click

    output = default_button_click(0)
    assert output[0] == "Dropdowns returned to default values. Click tick to assign."
