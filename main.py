import flet as ft
import random
import threading

imageSource = ""
imageDestination = ""
idSource = 0
idDestination = 0

width = 8
score = 0
candyImages = [
    "assets/red-candy.png",
    "assets/yellow-candy.png",
    "assets/orange-candy.png",
    "assets/purple-candy.png",
    "assets/green-candy.png",
    "assets/blue-candy.png",
]


def main(page: ft.Page):
    page.title = "Sweet Crush"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0
    page.window_height=700
    page.window_width=950
    page.window_resizable=False
    page.update()
    
   

    def checkRowForFour():
        global score
        for i in range(61):
            rowOfFour = [i, i + 1, i + 2, i + 3]
            decidedImage = squares.controls[i].image_src
            isBlank = True if squares.controls[i].image_src == "" else False
            notValid = [
                5,
                6,
                7,
                13,
                14,
                15,
                21,
                22,
                23,
                29,
                30,
                31,
                37,
                38,
                39,
                45,
                46,
                47,
                53,
                54,
                55,
            ]
            if i in notValid:
                continue
            if all(
                [
                    (squares.controls[index].image_src == decidedImage and not isBlank)
                    for index in rowOfFour
                ]
            ):
                score += 4
                score_display.value = str(score)
                for i in rowOfFour:
                    squares.controls[i].image_src = ""
        page.update()

    def checkColumnForFour():
        global score
        global width
        for i in range(40):
            columnOfFour = [i, i + width, i + width * 2, i + width * 3]
            decidedImage = squares.controls[i].image_src
            isBlank = True if squares.controls[i].image_src == "" else False
            if all(
                [
                    (squares.controls[index].image_src == decidedImage and not isBlank)
                    for index in columnOfFour
                ]
            ):
                score += 4
                score_display.value = str(score)
                for i in columnOfFour:
                    squares.controls[i].image_src = ""
        page.update()

    def checkRowForThree():
        global score
        for i in range(62):
            rowOfThree = [i, i + 1, i + 2]
            decidedImage = squares.controls[i].image_src
            isBlank = True if squares.controls[i].image_src == "" else False
            notValid = [6, 7, 14, 15, 22, 23, 30, 31, 38, 39, 46, 47, 54, 55]
            if i in notValid:
                continue
            if all(
                [
                    (squares.controls[index].image_src == decidedImage and not isBlank)
                    for index in rowOfThree
                ]
            ):
                score += 3
                score_display.value = str(score)
                for i in rowOfThree:
                    squares.controls[i].image_src = ""
        page.update()

    def checkColumnForThree():
        global score
        global width
        for i in range(48):
            columnForThree = [i, i + width, i + width * 2]
            decidedImage = squares.controls[i].image_src
            isBlank = True if squares.controls[i].image_src == "" else False
            if all(
                [
                    (squares.controls[index].image_src == decidedImage and not isBlank)
                    for index in columnForThree
                ]
            ):
                score += 3
                score_display.value = str(score)
                for i in columnForThree:
                    squares.controls[i].image_src = ""
        page.update()

    def moveIntoSquareBelow():
        global width
        # drop candies once some have been cleared
        for i in range(56):
            if squares.controls[i + width].image_src == "":
                squares.controls[i + width].image_src = squares.controls[i].image_src
                squares.controls[i].image_src = ""
                firstRow = [0, 1, 2, 3, 4, 5, 6, 7]
                isFirstRow = True if i in firstRow else False
                if isFirstRow and squares.controls[i].image_src == "":
                    randomImage = random.choice(candyImages)
                    squares.controls[i].image_src = randomImage
        page.update()

    def check_infinite():
        checkRowForFour()
        checkColumnForFour()
        checkRowForThree()
        checkColumnForThree()
        moveIntoSquareBelow()

    def setInterval(func, time):
        e = threading.Event()
        while not e.wait(time):
            func()

    def exchange():
        global imageSource
        global imageDestination
        global idSource
        global idDestination
        global width
        # Is a valid move?
        validMoves = [idSource - 1, idSource - width, idSource + 1, idSource + width]
        if idDestination in validMoves:  # To move
            squares.controls[idDestination].image_src = imageSource
            squares.controls[idSource].image_src = imageDestination
            squares.controls[idDestination].update()
            squares.controls[idSource].update()

        squares.controls[idSource].bgcolor = ""
        squares.controls[idDestination].bgcolor = ""
        squares.controls[idDestination].update()
        squares.controls[idSource].update()
        imageSource = ""
        imageDestination = ""
        idSource = 0
        idDestination = 0

    def clickCandy(e):
        global imageSource
        global imageDestination
        global idSource
        global idDestination
        e.control.bgcolor = "black54"
        e.control.update()
        if imageSource == "":
            imageSource = e.control.image_src
            idSource = e.control.key
        else:
            imageDestination = e.control.image_src
            idDestination = e.control.key
            exchange()

    def createBoard():
        grid = ft.GridView(
            expand=None,
            runs_count=8,
            max_extent=70,
            child_aspect_ratio=1.0,
            spacing=0,
            run_spacing=0,
            width=560,
            height=560,
        )
        for i in range(width * width):
            randomImage = random.choice(candyImages)
            square = ft.Container(
                key=i,
                image_src=randomImage,
                width=50,
                height=50,
                border_radius=5,
                on_click=clickCandy,
            )
            grid.controls.append(square)
        return grid

    # UI Game
    score_display = ft.Text("0", size=30,weight=ft.FontWeight.BOLD)
    squares = createBoard()

    page.add(
        ft.Container(
            
            width=page.width,
            height=page.height,
            padding=20,
            image_src="assets/background.png",
            image_fit=ft.ImageFit.FILL,
            alignment=ft.alignment.center,
            content=ft.Row(width=900,height=700,
                controls=[
                    ft.Container(
                        border=ft.border.all(3, "white54"),
                        border_radius=10,
                        width=150,
                        height=130,
                        bgcolor=ft.colors.PINK_ACCENT,
                        content=ft.Column(
                            [
                                ft.Text("Score", size=30,weight=ft.FontWeight.BOLD),
                                score_display,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(width=100),
                    ft.Container(
                        width=580,
                        height=580,
                        border_radius=10,
                        bgcolor="#a58cc3",
                        content=squares,
                        alignment=ft.alignment.center,
                    ),
                ]
            ),
           
        )
    )
    setInterval(check_infinite, 0.10)

if __name__=="__main__":
    ft.app(target=main)


