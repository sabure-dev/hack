import flet as ft


def main(page):
    page.title = "Вход"
    page.theme_mode = 'light'
    page.window.title_bar_hidden = False
    page.window.frameless = False
    page.window.height = 540
    page.window.width = 960
    page.window.resizable = False

    page.window.center()

    login = ft.Ref[ft.TextField]()
    password = ft.Ref[ft.TextField]()

    def theme_changed(e):
        if page.theme_mode == 'light':
            page.theme_mode = 'dark'
        else:
            page.theme_mode = 'light'
        c.label = (
            "Светлая тема" if page.theme_mode == 'light' else "Темная тема"
        )
        page.update()

    def btn_sign_in():
        page.update()
        login.current.focus()

    def btn_sign_up():
        page.update()
        login.current.focus()

    c = ft.Switch(label="Светлая тема", on_change=theme_changed)

    enter_row = ft.Row(
        [ft.ElevatedButton("Войти", on_click=btn_sign_in)],
        width=300,
        alignment=ft.MainAxisAlignment.END,

    )
    page.add(
        ft.Container(
            ft.Row(
                [c],
                alignment=ft.MainAxisAlignment.START,
            )

        ),
        ft.Container(
            ft.Column(
                [ft.Text("Hackhatons", size=32, font_family="Bauhaus LT(RUS BY LYAJKA)",), ft.TextField(ref=login, label="Логин", autofocus=True, width=300),
                 ft.TextField(ref=password, label="Пароль", password=True, can_reveal_password=True, width=300),
                 enter_row,
                 ft.Row([ft.Text("Нет аккаунта?", size=14)], width=300, alignment=ft.MainAxisAlignment.CENTER),
                 ft.Row([ft.ElevatedButton("Зарегистрироваться", on_click=btn_sign_up)], width=300, alignment=ft.MainAxisAlignment.CENTER)],
                height=405,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        )
    )


ft.app(target=main)
