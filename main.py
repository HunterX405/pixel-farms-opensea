from nicegui import app, ui
import farms_page, pets_page

def main():

    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        with ui.row():
            ui.button('Farms', on_click=lambda: ui.open('/farms'))
            ui.button('Pets', on_click=lambda: ui.open('/pets'))

    app.on_exception(print)
    ui.run(title='Pixels', dark=True, reload=False, tailwind=False)

main()
    