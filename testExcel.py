import openpyxl

#create a workbook

wb = openpyxl.Workbook()

# select the active sheet

sheet = wb.active

# write data to the sheet

sheet['A1'] = "name"
sheet['B1'] = "age"
sheet['A2'] = "John"
sheet['B2'] = 25
sheet['A3'] = "Mary"
sheet['B3'] = 30

# save the file

wb.save("test.xlsx")


