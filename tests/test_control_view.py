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
            buttons[4],
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
    buttons = [1, None, None, None, None]
    button_id = "button_update"

    ctx = copy_context()
    patched_assign_sections = mocker.patch("app.core_api.assign_sections")
    output = ctx.run(run_callback)
    patched_assign_sections.assert_called_once()
    assert output[0] == "Clicked Update Button!"

    """Test Default Button."""
    buttons = [None, 1, None, None, None]
    button_id = "button_default"

    ctx = copy_context()
    output = ctx.run(run_callback)
    assert output[0] == "Clicked Default Button!"

    """Test Start Button."""
    buttons = [None, None, 1, None, None]
    button_id = "button_start"

    ctx = copy_context()
    output = ctx.run(run_callback)
    assert output[0] == "Clicked Start Button!"

    """Test Stop Button."""
    buttons = [None, None, None, 1, None]
    button_id = "button_stop"

    ctx = copy_context()
    output = ctx.run(run_callback)
    assert output[0] == "Clicked Stop Button!"

    """Test Restart Button."""
    buttons = [None, None, None, None, 1]
    button_id = "button_restart"

    ctx = copy_context()
    patched_refresh_sections = mocker.patch("app.core_api.refresh_sections")
    output = ctx.run(run_callback)
    patched_refresh_sections.assert_called_once()
    assert output[0] == "Clicked Restart Button!"
