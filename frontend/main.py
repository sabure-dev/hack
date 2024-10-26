import flet as ft


def main(page):
    page.title = "Вход в Hackwars"
    page.theme_mode = 'light'
    page.route = "/login"
    page.window.title_bar_hidden = False
    page.window.frameless = False
    page.window.height = 620
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

    def btn_alredy_have(e):
        page.route = "/login"
        page.update()
        login.current.focus()

    def btn_havent(e):
        page.route = "/register"
        page.update()
        login.current.focus()

    def btn_sign_in(e):
        page.update()
        login.current.focus()

    def btn_sign_up(e):
        page.update()
        login.current.focus()

    c = ft.Switch(label="Светлая тема", on_change=theme_changed)
    hackwars = ft.Row([ft.Text("Hackwars", size=64, font_family="Bauhaus LT(RUS BY LYAJKA)")],
                               alignment=ft.MainAxisAlignment.CENTER)
    enter_row = ft.Row(
        [ft.ElevatedButton("Войти", on_click=btn_sign_in)],
        width=300,
        alignment=ft.MainAxisAlignment.END,

    )
    reg_row = ft.Row(
        [ft.ElevatedButton("Зарегистрироваться", on_click=btn_sign_up)],
        width=300,
        alignment=ft.MainAxisAlignment.END,

    )
    page.add(

    )

    def route_change(route):
        page.views.clear()
        page.title = "Вход в Hackwars"
        page.views.append(
            ft.View(
                "/login",
                [
                    ft.Container(
                        ft.Row(
                            [c],
                            alignment=ft.MainAxisAlignment.START,
                        )

                    ),
                    hackwars,
                    ft.Container(
                        ft.Column(
                            [
                             ft.Text("Вход", size=28, font_family="Bauhaus LT(RUS BY LYAJKA)"),
                             ft.TextField(ref=login, label="Логин", autofocus=True, width=300),
                             ft.TextField(ref=password, label="Пароль", password=True, can_reveal_password=True,
                                          width=300),
                             enter_row,
                             ft.Row([ft.Text("Нет аккаунта?", size=14)], width=300,
                                    alignment=ft.MainAxisAlignment.CENTER),
                             ft.Row([ft.ElevatedButton("Зарегистрироваться", on_click=btn_havent)], width=300,
                                    alignment=ft.MainAxisAlignment.CENTER)],
                            height=405,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        alignment=ft.alignment.center,
                    ),
                ],
            )
        )
        if page.route == '/register':
            page.title = "Регистрация в Hackwars"
            page.views.append(
                ft.View(
                    "/register",
                    [
                        ft.Container(
                            ft.Row(
                                [c],
                                alignment=ft.MainAxisAlignment.START,
                            )

                        ),
                        hackwars,
                        ft.Container(
                            ft.Column(
                                [ft.Text("Регистрация", size=32, font_family="Bauhaus LT(RUS BY LYAJKA)", ),
                                 ft.TextField(ref=login, label="Логин", autofocus=True, width=300),
                                 ft.TextField(ref=password, label="Пароль", password=True, can_reveal_password=True,
                                              width=300),
                                 ft.TextField(ref=password, label="Повторите пароль", password=True, can_reveal_password=True,
                                              width=300),
                                 reg_row,
                                 ft.Row([ft.Text("Есть аккаунт?", size=14)], width=300,
                                        alignment=ft.MainAxisAlignment.CENTER),
                                 ft.Row([ft.ElevatedButton("Войти", on_click=btn_alredy_have)], width=300,
                                        alignment=ft.MainAxisAlignment.CENTER)],
                                height=405,
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            alignment=ft.alignment.center,
                        ),
                    ],
                )
            )
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


ft.app(target=main)
