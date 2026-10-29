from funcs import splice
import easyfileio

origPlanFile = easyfileio.content('ConvertPlan', 'inputPlan.txt')
newPlan = easyfileio.content('ConvertPlan', 'outputPlan.txt')
origPlan = origPlanFile.fetch(no_strip=True)
newPlan.fetch()
revPlan = []

if origPlan == []:
    input('enter in file')

else:
    for i in origPlan:
        planHalf, temp = splice.splice(i, '#', 'str')
        plan = f'{planHalf}フリー'
        revPlan.append(plan)


    overwrite = 'None'
    for ilen ,i in enumerate(revPlan):
        if ilen == 0:
            overwrite = '*overwrite*'
        else:
            overwrite = 'None'
        print(i)
        newPlan.save(i, overwrite)