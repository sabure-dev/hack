import flet as ft

fonts = {
    "Bauhaus": "fonts/bauhas_lt(RUS BY LYAJKA).ttf",
    "NanumGothic": "fonts/NanumGothic-Regular.ttf"
}


def main(page):
    global fonts
    page.title = "Вход в Hackwars"
    page.theme_mode = 'light'
    page.fonts = fonts
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
    hackwars = ft.Row([ft.Text("Hackwars", size=64, font_family="Bauhaus")],
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
                                ft.Text("Вход", size=28, font_family="NanumGothic"),
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
                                [ft.Text("Регистрация", size=28, font_family="NanumGothic", ),
                                 ft.TextField(ref=login, label="Логин", autofocus=True, width=300),
                                 ft.TextField(ref=password, label="Пароль", password=True, can_reveal_password=True,
                                              width=300),
                                 ft.TextField(ref=password, label="Повторите пароль", password=True,
                                              can_reveal_password=True,
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


def jury(page):
    global fonts
    page.title = "Оценить команды"
    page.theme_mode = 'light'
    page.window.height = 1080
    page.window.width = 1920
    page.route = "/rate"
    page.fonts = fonts
    points1 = ft.Ref[ft.TextField]()
    _filter = ft.InputFilter('^[0-5]?$')

    t1p1 = ft.TextField(input_filter=_filter, ref=points1, label='Критерий 1', width=123)
    t1p2 = ft.TextField(input_filter=_filter, ref=points1, label='Критерий 2', width=123)
    t1p3 = ft.TextField(input_filter=_filter, ref=points1, label='Критерий 3', width=123)
    t1p4 = ft.TextField(input_filter=_filter, ref=points1, label='Критерий 4', width=123)
    t1p5 = ft.TextField(input_filter=_filter, ref=points1, label='Критерий 5', width=123)
    t1p6 = ft.TextField(input_filter=_filter, ref=points1, label='Критерий 6', width=123)
    t1p7 = ft.TextField(input_filter=_filter, ref=points1, label='Критерий 7', width=123)
    t1p8 = ft.TextField(input_filter=_filter, ref=points1, label='Критерий 8', width=123)
    t1p9 = ft.TextField(input_filter=_filter, ref=points1, label='Критерий 9', width=123)
    t1p10 = ft.TextField(input_filter=_filter, ref=points1, label='Критерий 10', width=123)

    t2p1 = ft.TextField(input_filter=_filter, ref=points1, label='Критерий 1', width=123)
    t2p2 = ft.TextField(input_filter=_filter, ref=points1, label='Критерий 2', width=123)
    t2p3 = ft.TextField(input_filter=_filter, ref=points1, label='Критерий 3', width=123)
    t2p4 = ft.TextField(input_filter=_filter, ref=points1, label='Критерий 4', width=123)
    t2p5 = ft.TextField(input_filter=_filter, ref=points1, label='Критерий 5', width=123)
    t2p6 = ft.TextField(input_filter=_filter, ref=points1, label='Критерий 6', width=123)
    t2p7 = ft.TextField(input_filter=_filter, ref=points1, label='Критерий 7', width=123)
    t2p8 = ft.TextField(input_filter=_filter, ref=points1, label='Критерий 8', width=123)
    t2p9 = ft.TextField(input_filter=_filter, ref=points1, label='Критерий 9', width=123)
    t2p10 = ft.TextField(input_filter=_filter, ref=points1, label='Критерий 10', width=123)


    def theme_changed(e):
        if page.theme_mode == 'light':
            page.theme_mode = 'dark'
        else:
            page.theme_mode = 'light'
        c.label = (
            "Светлая тема" if page.theme_mode == 'light' else "Темная тема"
        )
        page.update()

    team1 = 'Команда 1'
    team2 = 'Команда 2'
    c = ft.Switch(label="Светлая тема", on_change=theme_changed)
    rate = ft.Row(
        [ft.Text(f"{team1}", size=64, font_family="NanumGothic"),
         ft.Text(f"{team2}", size=64, font_family="NanumGothic")],
        width=1920,
        alignment=ft.MainAxisAlignment.SPACE_AROUND)

    def show_criteria(e):
        page.dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                content=ft.Text("Критерии оценки:\n"
                                "1.Технические навыки участников\n"
                                "2.Реакция на инциденты\n"
                                "3.Анализ угроз\n"
                                "4.Командная работа\n"
                                "5.Документация и отчетность\n"
                                "6.Этика и соблюдение норм\n"
                                "7.Креативность и инновации\n"
                                "8.Знание теоритечской части\n"
                                "9.Практические задания\n"
                                "10.Обратная связь и самоанализ:\n"
                                "По каждому критерию оценка выставляется от 0 до 5 баллов\n", font_family="NanumGothic"),
                padding=20,
                width=300,
                height=400
            ),
            actions=[
                ft.TextButton("Закрыть", on_click=lambda e: page.close(page.dialog))
            ]
        )
        page.dialog.open = True
        page.update()
    def submit(e):
        s1 = (int(t1p1.value or 0) + int(t1p2.value or 0) + int(t1p3.value or 0) + int(t1p4.value or 0) + int(t1p5.value or 0) + int(t1p6.value or 0) +
        int(t1p7.value or 0) + int(t1p8.value or 0) + int(t1p9.value or 0) + int(t1p10.value or 0))
        s2 = (int(t2p1.value or 0) + int(t2p2.value or 0) + int(t2p3.value or 0) + int(t2p4.value or 0) + int(t2p5.value or 0) + int(t2p6.value or 0) +
        int(t2p7.value or 0) + int(t2p8.value or 0) + int(t2p9.value or 0) + int(t2p10.value or 0))
        print(f'{team1} = {s1}')
        print(f'{team2} = {s2}')
    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View('/rate',
                    [
                        ft.Container(
                            ft.Row(
                                [rate],
                                width=1920
                            ),
                        ),
                        ft.Row(
                            [ft.Column([t1p1, t1p2, t1p3, t1p4, t1p5, t1p6, t1p7, t1p8, t1p9, t1p10
                                        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                             ft.VerticalDivider(width=10, thickness=4),
                             ft.Column([t2p1, t2p2, t2p3, t2p4, t2p5, t2p6, t2p7, t2p8, t2p9, t2p10
                                        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)],
                            width=1920,
                            height=680,
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        ),
                        ft.Row(
                            [ft.Column(
                                [c],
                                height=175,
                                alignment=ft.MainAxisAlignment.END
                            ),
                            ft.ElevatedButton('Выставить баллы!', on_click=submit),
                            ft.Column(
                                [ft.ElevatedButton('Критерии оценки', on_click=show_criteria)],
                                height=175,
                                alignment=ft.MainAxisAlignment.END)
                            ],
                            width=1920,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    ]
                    )
        )
        page.title = "Вход в Hackwars"
        page.update()

    page.on_route_change = route_change
    page.go(page.route)
    page.update()


ft.app(target=jury)
