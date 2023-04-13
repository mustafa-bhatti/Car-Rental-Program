import PySimpleGUI as sg

car_list = ["Cultus", "Swift", "Yaris", "Civic"]
cultus_avail = 2  # initialises values
swift_avail = 3
yaris_avail = 2
civic_avail = 7
car = []
bg, rent, insurance, tax, days, total, T_income, T_tax, T_Insurance = 0, 0, 0, 0, 0, 0, 0, 0, 0
total_cars = []
left_s = [  # left column
    [sg.T("Select Function")],
    [sg.B("Car Rental", key="-C.Rent-")],
    [sg.B("Car Return", key="-C.Return-")],
    [sg.B("Total Finance Detail", key="-F.Detail-")]
]
header = ["Model", "Available", "Price/Day", "Liability Insurance/Day", "Comprehensive Insurance/Day"]
rows = [  # main table data
    ["Cultus", cultus_avail, 3500, 300, 550],
    ["Swift", swift_avail, 5000, 470, 590],
    ["Yaris", yaris_avail, 5700, 600, 650],
    ["Civic", civic_avail, 7500, 700, 750]
]
select_car = [
    [sg.T("Select Car:", key="-T.text.-")],
    [sg.Table(values=rows, headings=header, enable_events=True, key="-C.Table-")],
    [sg.T("Number of Days "), sg.I(default_text=1, key="NumDays", size=(20, 1))],
    [sg.T("Select Insurance :")],
    [sg.Radio(text="Liability", group_id="radio", enable_events=True, default=True, key="L")],  # Radio Buttons
    [sg.Radio(text="Comprehensive", group_id="radio", enable_events=True, key="C")],
    [sg.B("Ok", key="Car-ok")],
    [sg.T("Error: Car Not Available", key="error-A", visible=False, text_color="red")],  # Error prompts
    [sg.T("Error: Select all parameters", key="error", visible=False, text_color="red")]
]
summary = [  # Summary Page
    [sg.T("Summary :")],
    [sg.T("Car", size=(20, 1)), sg.Text("Car Name", key="-S.Car-", justification="right", )],
    [sg.T("Rent Cost", size=(20, 1)), sg.Text("Rent", key="-S.Rent-", justification="right")],
    [sg.T("Insurance Cost", size=(20, 1)), sg.Text("Insurance", key="-S.Insur-", justification="right")],
    [sg.T("Tax", size=(20, 1)), sg.Text("Tax", key="-S.Tax-", justification="right")],
    [sg.T("------------------------------------------\n------------------------------------------")],
    [sg.T("Total", size=(20, 1)), sg.Text("Car Name", key="-S.Total-", justification="right")],
    [sg.B("Confirm", button_color="green", key="S.Confirm"), sg.Cancel(key="S.Cancel")]
]
c_return = [  # Return Page
    [sg.T("Select Car :")],
    [sg.DD(car_list, default_value=car_list[0], size=(27, 1), key="DD", enable_events=True)],  # DropDown Menu
    [sg.B("Return", key="-return-")]
]
header_Fin = ["Car Model", "Rent Cost", "Days", "Insurance Cost", "Tax Cost", "Total Cost"]

Fin_Detail = [  # Total Financial Detail Page
    [sg.Table(headings=header_Fin, values=total_cars, key="finDetail")],
    [sg.T("Total Income : "), sg.T("0", key="T_income")],
    [sg.T("Total Tax : "), sg.T("0", key="T_tax")],
    [sg.T("Total Insurance : "), sg.T("0", key="T_insurance")],
]
layout = [  # Layout Details
    [sg.Text("TG Enterprises", justification="center", size=(80, 1), font=30, text_color="yellow")],  # Header
    [sg.Col(left_s, size=(140, 200)), sg.VSeparator(),
     sg.Col(select_car, visible=False, key="-SelectCar-"),  # Different pages with their keys
     sg.Col(summary, visible=False, key="-Summary-"),
     sg.Col(c_return, visible=False, key="-Return-"),
     sg.Col(Fin_Detail, visible=False, key="-FinDetail-")]
]
window = sg.Window("TG Enterprises", layout)
while True:  # While loop to make the window persistent
    events, values = window.read()
    print(events, values)  # Printing values for debugging process
    if events == sg.WIN_CLOSED:  # Closes window
        window.close()
        break
    elif events == "-C.Rent-":
        window.Element("-SelectCar-").update(visible=True)  # shows the rent page and makes all other pages invisible
        window.Element("-Summary-").update(visible=False)
        window.Element("-Return-").update(visible=False)
        window.Element("-FinDetail-").update(visible=False)
        window.Element("error").update(visible=False)
        window.Element("error-A").update(visible=False)

    elif events == "Car-ok":
        if values["-C.Table-"]:  # check if a row is clicked
            bg = str(values["-C.Table-"])
            bg = int(bg[1])
            car = rows[int(bg)]
            days = int(values["NumDays"])  # Updates Values
            if car[1] == 0:
                window.Element("error-A").update(visible=True)
            elif days == 0:
                window.Element("error").update(visible=True)
            else:
                window["-S.Car-"].update(car[0])
                rent = car[2] * days
                window["-S.Rent-"].update(str(car[2]) + " PKR")
                tax = rent * 0.05
                window["-S.Tax-"].update(str(tax) + " PKR")

                if values["L"]:
                    insurance = car[3]
                    window["-S.Insur-"].update(str(car[3]) + " PKR")
                else:
                    insurance = car[4]
                    window["-S.Insur-"].update(str(car[4]) + " PKR")
                total = rent + insurance + tax
                window["-S.Total-"].update(str(total) + " PKR")

                window.Element("-Summary-").update(visible=True)
                window.Element("-SelectCar-").update(visible=False)
                window.Element("-Return-").update(visible=False)
                window.Element("-FinDetail-").update(visible=False)
        else:
            window.Element("error").update(visible=True)
    elif events == "S.Confirm":  # Removes one car from the inventory
        if car[0] == "Cultus":
            cultus_avail -= 1
            rows[bg][1] = cultus_avail
            window["-C.Table-"].update(values=rows)
        if car[0] == "Swift":
            swift_avail -= 1
            rows[bg][1] = swift_avail
            window["-C.Table-"].update(values=rows)
        if car[0] == "Yaris":
            yaris_avail -= 1
            rows[bg][1] = yaris_avail
            window["-C.Table-"].update(values=rows)
        if car[0] == "Civic":
            civic_avail -= 1
            rows[bg][1] = civic_avail
            window["-C.Table-"].update(values=rows)
        total_cars.append([car[0], car[2], days, insurance, tax, total])
        T_tax += tax
        T_income += rent
        T_Insurance += insurance
        window["T_income"].update(str(T_income) + " PKR")
        window["T_tax"].update(str(T_tax) + " PKR")
        window["T_insurance"].update(str(T_Insurance) + " PKR")
        window["finDetail"].update(values=total_cars)  # Updates the Total Fin Values
        window.Element("-Return-").update(visible=False)
        window.Element("-SelectCar-").update(visible=False)
        window.Element("-Summary-").update(visible=False)
        window.Element("-FinDetail-").update(visible=False)
    elif events == "S.Cancel":
        window.Element("-Return-").update(visible=False)
        window.Element("-SelectCar-").update(visible=True)
        window.Element("-Summary-").update(visible=False)
        window.Element("-FinDetail-").update(visible=False)
    elif events == "-C.Return-":
        window.Element("-Return-").update(visible=True)
        window.Element("-SelectCar-").update(visible=False)
        window.Element("-Summary-").update(visible=False)
        window.Element("-FinDetail-").update(visible=False)
    elif events == "-return-":  # Returns the car
        if values["DD"] == "Cultus":
            cultus_avail += 1
            rows[0][1] = cultus_avail
            window["-C.Table-"].update(values=rows)
        if values["DD"] == "Swift":
            swift_avail += 1
            rows[1][1] = swift_avail
            window["-C.Table-"].update(values=rows)
        if values["DD"] == "Yaris":
            yaris_avail += 1
            rows[2][1] = yaris_avail
            window["-C.Table-"].update(values=rows)
        if values["DD"] == "Civic":
            civic_avail += 1
            rows[3][1] = civic_avail
            window["-C.Table-"].update(values=rows)
    elif events == "-F.Detail-":  # Shows the Total Fin Page
        window.Element("-FinDetail-").update(visible=True)
        window.Element("-Return-").update(visible=False)
        window.Element("-SelectCar-").update(visible=False)
        window.Element("-Summary-").update(visible=False)
window.close()
