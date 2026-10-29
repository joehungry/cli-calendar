timestamp = 0
dateTypLoc = 1
dateNAMELoc = 2
dateSTARTSHOWINGLoc = 3
dateDATELoc = 4
dateTIMELoc = 5
dateTIMEENDLoc = 6
dateEXPIRESTARTLoc = 7
dateEXPIREENDLoc = 8
dateDAYLoc = 9
dateREMINDERLoc = 10
dateDONELoc = 11

import dotenv, os
import supabase, easyfileio, datetime
from funcs import num

dayRightNow = datetime.datetime.now()
fDayRightNow = f'{dayRightNow.year}/{dayRightNow.month}/{dayRightNow.day}'
dayRightNowNum = num.numify(fDayRightNow)
timeRightNow = num.numify(f'{fDayRightNow} {dayRightNow.hour}:{dayRightNow.minute}')

class get_cloud:
    def __init__(self, supabaseURL, supabaseKey):
        dotenv.load_dotenv('supabaseLoginInfo/cloudLoginInfo.env')
        self.supabaseURL = supabaseURL
        self.supabaseKey = supabaseKey
        self.plans_to_remove = []
        self.plans_to_save = []
        self.plans_to_update = []
        self.program_instance = 'starting'

    async def initialize_cloud(self):
        self.program_instance = 'initalizing'
        self.cloud_client: supabase.AsyncClient = await supabase.acreate_client(self.supabaseURL, self.supabaseKey)

    async def load_cloud(self, table_name, get_element):
        cloud_var = await self.cloud_client.table(table_name).select(get_element).execute()
        if cloud_var.data:
            return cloud_var.data
        return {}
            
    async def save_plans_from_cloud(self, table_name, local_plan_raw: list):
        self.program_instance = 'saving new plans'
        local_timestamp = [easyfileio.de_stringify_list(plan, ',')[timestamp] for plan in local_plan_raw]
        save_to_local = ''
        online_saved_plans = await self.load_cloud(table_name, '*')
        for i in online_saved_plans:
            online_plan = easyfileio.stringify_list([i['timestamp'], i['plan_type'], i['name'], i['start_date'], i['date'], i['time'], i['end_time'], None,None,i['weekday'],i['set_reminder'],0], ',')
            if str(i['timestamp']) in local_timestamp:
                pass
            elif i != online_saved_plans[len(online_saved_plans)-1]:
                local_plan_raw.append(online_plan)
                save_to_local += f'{online_plan}\n'
                self.plans_to_remove.append(i['timestamp'])
            else:
                local_plan_raw.append(online_plan)
                save_to_local += f'{online_plan}'
                self.plans_to_remove.append(i['timestamp'])
        return local_plan_raw, save_to_local

    def remove_expired_plans(self, planDateContentRaw):
        self.program_instance = 'removing expired plans'
        correctLen = -1
        removeLocalPlans = []
        planDateContent = []
        for i in planDateContentRaw:
            correctLen += 1
            iToList = easyfileio.de_stringify_list(i, ',')
            if iToList[dateTIMELoc] == None:
                iplanTime = '23:59'
            else:
                iplanTime = iToList[dateTIMELoc]
            planTimeNum = num.numify(f'{iToList[dateDATELoc]} {iplanTime}')
            expireStartNum = num.numify(iToList[dateEXPIRESTARTLoc])
            expireEndNum = num.numify(iToList[dateEXPIREENDLoc])
            if planTimeNum < timeRightNow and (not iToList[dateDATELoc] == True):
                removeLocalPlans.append(correctLen)
                correctLen -= 1
            elif not iToList[dateTypLoc] == 0: #typeが1か2だったら無条件でアペンドして（1.2だったらexpiredateはオンラインでの催促の期間）
                planDateContent.append(iToList)
            elif not iToList[dateEXPIRESTARTLoc] == None and expireEndNum < dayRightNowNum: #expiredateがある場合は、EXPIREENDNUMをみてよってこと
                removeLocalPlans.append(correctLen)
            elif expireStartNum > dayRightNowNum:
                pass
            else:
                planDateContent.append(iToList)
        return planDateContent, removeLocalPlans


    async def check_cloud_plans(self, table_name, local_content):
        self.program_instance = 'updating online plans'
        main_cloud_plans = await self.load_cloud(table_name, '*')
        main_cloud_plans_key_list = [plan['timestamp'] for plan in main_cloud_plans]
        main_cloud_plans_value_list = [plan for plan in main_cloud_plans]
        local_primary_key = []
        self.plans_to_save = []
        self.plans_to_remove = []
        self.plans_to_update = []
        for plan in local_content:
            local_primary_key.append(plan[timestamp])
            if plan[dateTIMELoc] == None:
                planTime = None
            else:
                hour, minute = plan[dateTIMELoc].split(':')
                planTime = f'{int(hour):02d}:{int(minute):02d}:00'
            if plan[dateTIMEENDLoc] == None:
                planTimeEnd = None
            else:
                hour, minute = plan[dateTIMEENDLoc].split(':')
                planTimeEnd = f'{int(hour):02d}:{int(minute):02d}:00'
            planDict = {'timestamp': plan[timestamp], 'dateNAME': plan[dateNAMELoc], 'dateSTARTSHOWING': 'true' if plan[dateSTARTSHOWINGLoc] == True else plan[dateSTARTSHOWINGLoc],'dateDATE': plan[dateDATELoc], 'dateTIME': planTime, 'dateDAY': plan[dateDAYLoc], 'dateTIMEEND': planTimeEnd, 'dateTYPE': plan[dateTypLoc], 'dateEXPIRESTART': plan[dateEXPIRESTARTLoc], 'dateEXPIREEND': plan[dateEXPIREENDLoc], 'dateDONE': str(plan[dateDONELoc])}
            if plan[dateREMINDERLoc] == False and plan[timestamp] in main_cloud_plans_key_list:
                self.plans_to_remove.append(plan[timestamp])
            elif plan[dateREMINDERLoc] == False:
                pass
            elif not plan[timestamp] in main_cloud_plans_key_list: #plan doesn't exist at all (indicator missing)
                self.plans_to_save.append(planDict)
            elif not planDict in main_cloud_plans_value_list: #plan does exist (indicator exists) but also plan is a little different than the thing on local
                self.plans_to_update.append(planDict)
            
        for primary_key in main_cloud_plans_key_list:
            if not primary_key in local_primary_key:
                self.plans_to_remove.append(primary_key)

    async def sync_online_plans(self, table):
        self.program_instance = 'updating online plans' #because this is the first step when updating online plans
        if not len(self.plans_to_remove) == 0:
            removed = await self.cloud_client.table(table).delete().in_("timestamp", self.plans_to_remove).execute()
        if not len(self.plans_to_save) == 0:
            saved = await self.cloud_client.table(table).insert(self.plans_to_save).execute()
        if not len(self.plans_to_update) == 0:
            upserted = await self.cloud_client.table(table).upsert(self.plans_to_update).execute()
        self.plans_to_remove = []
        self.plans_to_save = []
        self.plans_to_update = []

    def return_instance(self):
        return self.program_instance

    async def main(self):
        try:
            await self.initialize_cloud()
            local_plan = easyfileio.content('calendar', 'planDateSettings.txt', encode='cp932')

            #updating local plans
            original_local_plan = local_plan.fetch()
            local_plan_full, plans_to_save_locally = await self.save_plans_from_cloud('plans_to_add', original_local_plan)
            if plans_to_save_locally != '':
                local_plan.save(plans_to_save_locally)
            updated_plans, remove_plan_index = self.remove_expired_plans(local_plan_full)
            _ = local_plan.fetch() #so that easyfileio gets the updated plans
            if not remove_plan_index == []:
                local_plan.delete_bulk(remove_plan_index)

            #updating cloud plans
            await self.sync_online_plans('plans_to_add') #im deleting the plans added online from (self.save_plans_from_cloud) <- this step
            await self.check_cloud_plans('plansTable', updated_plans)
            await self.sync_online_plans('plansTable')

            self.program_instance = 'finished'
        except:
            exit()

async def local_main():
    from funcs import prints
    import asyncio

    dotenv.load_dotenv('supabaseLoginInfo/cloudLoginInfo.env')
    supabaseURL = os.getenv("SUPABASE_URL")
    supabaseKey = os.getenv("SUPABASE_KEY")
    sync_plans = get_cloud(supabaseURL, supabaseKey)
    asyncio.create_task(sync_plans.main())
    loading_num = 1
    while True:
        update_instance = sync_plans.return_instance()
        if update_instance != 'finished':
            prints.loading(loading_num)
            print(f'{update_instance}...')
        else:
            break
        loading_num += 1
        await asyncio.sleep(0.5)
    os.system('cls')
    input(update_instance)


if __name__ == '__main__':
    import asyncio
    asyncio.run(local_main())
