url = "http://127.0.0.1:5000/v1/chat/completions"
headers = {"Content-Type": "application/json"}

replaces_datamap = {
    '&quot;': '"',
    '&lt; &lt;': '"',
    '&gt; &gt;': '"',
    ' &apos; s': "'s",
    ' &apos;': "'",
    '&gt;': '',
    '&lt;': '',
    ' &amp; ': '&',
    '&amp;': '&',
    'CGN-\n': 'CGN-'
}
post_replaces_datamap = {
    '  ': ' ',
    ' "': '"',
    '" ': '"',
    ' ,': ',',
    ' & ': '&'
}


def cleanup(text):
    for k, v in replaces_datamap.items():
        text = text.replace(k, v)
    for k, v in post_replaces_datamap.items():
        text = text.replace(k, v)
    return text


llm_params = {
    "mode": "instruct",
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.9,
    "min_p": 0,
    "top_k": 20,
    "repetition_penalty": 1.15,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "repetition_penalty_range": 1024,
    "typical_p": 1,
    "tfs": 1,
    "top_a": 0,
    "epsilon_cutoff": 0,
    "eta_cutoff": 0,
    "guidance_scale": 1,
    "mirostat_mode": 0,
    "mirostat_tau": 5,
    "mirostat_eta": 0.1,
    "skip_special_tokens": True,
    "seed": 42,
    "user": "You",
    "character": "Assistant",
}

base_prompt_data = """
I will print an information blocks containing data about the contract. Your goal: to analyze and structure information in the form of:
contract_id: (starting with CGN-)
contrtact_short_summary: basic information about the work or services to be performed, the type of work or service
contract_start_date: start date of work under the contract
contract_deadline_date: date by which the contract must be completed
contract_geo: contract object location
tag_construction: 1 if construction work will be carried out under the contract else 0
tag_energy_not_nuclear: 1 if the contract is related to energy facilities (except nuclear) else 0
tag_nuclear power: 1 if the contract is related to nuclear energy facilities else 0
tag_electronics_supply_installation: 1 if the contract is includes to the supply or installation of electronics else 0
tag_materials_supplies: 1 if the contract is includes to the supply of materials else 0
tag_equipment_supply_installation: 1 if the contract is includes to the supply or installation of equipment else 0
tag_research_design_works: 1 if the contract includes research or design work else 0
tag_chemical_production: 1 if the contract includes to the supply of chemical production else 0
tag_other_services: 1 if the contract includes other service work besides those listed above else 0

Example of a jobs well done:

input:
Синьцзян-Китайская база экологически чистой энергии в Синьцзяне, Лоуп, 1 млн. кВт оптико-волнового поля PC
(Контингент: CGN-202307050014)
Территория, в которой находятся тендерные проекты: Синьцзян-Уйгурский автономный район и Тэгу, округ Лоуп
Условия торгов
В рамках этого проекта на базе экологически чистой энергетики в Синьцзяне в Лоупе 1 млн. кВт (проект тендера)
Номер: CGN-202307050014, одобренный подразделением по утверждению проектов, финансируется за счет средств, полученных от предприятия, и реализовано, торгующее
China Solar Energy Successing Ltd. В рамках этого проекта уже имеются условия для проведения торгов и в настоящее время проводятся открытые торги.
II. ОБЩИЙ ОБЗОР ПРОЕКТОВ, ОГРАНИЧЕННОСТИ И ПЛАНИРОВАНИЯ ПРОЕКТОВ
Размер проекта:
Синьцзян-цзян, Китай, Новая энергетическая база мощностью 1 000 000 000 000 000 000 000 кигаваттских люминесцентных оптических дисков в районе Лоуп
Место планирования расположено в юго-западном пригороде округа Лоуп, который расположен примерно в 22 км к юго-востоку от города Теда, в районе площадью Гоби-Бич, в пределах участка.
Общий контрактный проект PC в 1 млн кВт-диапазоне на базе экологически чистой энергии в Синьцзяне разделен на два пакета из четырех.
ii) упорядочение последовательности кандидатов, указанных в пунктах назначения в пакете с минимальными суммами, и в том же пункте, в котором объединенная позиция основывается на предыдущем месте
Участники торгов, которые не были рекомендованы в качестве первого кандидата в соответствии с настоящим пунктом или другим пунктом в той же упаковке, не должны иметь права на участие в торгах после того, как они были отобраны.
В этом пункте рекомендуется быть первым кандидатом. За исключением тех случаев, когда в соответствии с вышеупомянутыми принципами корректируется первоначальная кандидатская баллотировка, остальные кандидаты, выигравшие конкурс, по-прежнему представлены в сводном порядке
Рекомендуется последовательность.
Подробная информация об объеме торгов содержится в тендерной технической документации.
Планируемый период:
Запланировано начать работу 15 августа 2023 года (в зависимости от того, какое время будет предшествовать уведомление на неделю), а 30 декабря 2023 года будет полностью произведена электроэнергия.
Подробная информация о требованиях в отношении конкретных узлов рабочего времени содержится в тендерной технической документации.

result:
contract_id: CGN-202307050014
contrtact_short_summary: Постройка энергетической базы. Экологически чистая энергетика.
contract_start_date: 2023-08-15
contract_deadline_date: 2023-12-30
contract_geo: Синьцзян-Уйгурский автономный район и Тэгу, округ Лоуп
tag_construction: 1
tag_energy_not_nuclear: 1
tag_nuclear power: 0
tag_electronics_supply_installation: 0
tag_materials_supplies: 0
tag_equipment_supply_installation: 0
tag_research_design_works: 0
tag_chemical_production: 0
tag_other_services: 0

input:
20230731_12345
Китайский документ 67-9trans.txt
Хубэй собирает тендер на строительство гидроэнергетической станции
(Контингент: CGN-202301310002)
Территория, в которой осуществляется тендерный проект: Хубэй, Хуанган, округ Чун
Условия торгов
В рамках проекта"Хубэй"велась работа по строительству гидроэнергетической станции (заявка на проект CGN-202301310002), которая была осуществлена по проекту
Утверждено подразделением по утверждению, проект финансируется за счет собственных средств предприятия и уже реализован, а тендер - за счет компании"Чайна нью-Энтерпрайз". Проект уже
При наличии условий для проведения торгов проводятся открытые торги.
II. ОБЩИЙ ОБЗОР ПРОЕКТОВ, ОГРАНИЧЕННОСТИ И ПЛАНИРОВАНИЯ ПРОЕКТОВ
Размер проекта:"Хубэй","Вай","Вэнвайн","Вай","Вэньгуань","Вэньчуань", провинция Хубэй, в коммуне Дуби, префектура,"Вэньчуань"и Дупи
Основными зданиями, построенными на узлах, являются водохранилища, водохранилища, системы водоснабжения, подземные сооружения и переключатели.
Содержание и объем торгов:
Содержание и сфера охвата данного тендера включают:
1) строительство и эксплуатация электростанций и их вспомогательных сооружений;
2) строительство электростанций 2, 3 и 4;
3) строительство дренажных отверстий и плотин.
В рамках этого проекта были проведены конкурсы на проведение строительных работ по генеральному подряду, включая строительство, закупку, отладку, приемку и обслуживание в рамках проекта. Конкретный объем торгов
Более подробную информацию см. в тендерной технической документации.
Планируемый период:
347 календарных дней
2.2 Дата начала работ 28 февраля 2023 года
2.3 Дата завершения проекта 10 февраля 2024 года

result:
contract_id: CGN-202301310002
contrtact_short_summary: Строительство гидроэлектростанции. Экологически чистая энергетика.
contract_start_date: 2023-02-28
contract_deadline_date: 2024-02-10
contract_geo: провинция Хубэй, в коммуне Дуби, префектура,"Вэньчуань"и Дупи
tag_construction: 1
tag_energy_not_nuclear: 1
tag_nuclear power: 0
tag_electronics_supply_installation: 0
tag_materials_supplies: 0
tag_equipment_supply_installation: 0
tag_research_design_works: 0
tag_chemical_production: 0
tag_other_services: 0

input:
Проект по закупке электрического оборудования в АТЦПТ (третий тендер) (номер тендера: CGN-202204240004-N2 Утвержден, проект финансируется за счет собственных средств предприятия и уже реализован, тендеры на поставку ядерной энергии в Гуанчжоу
Ltd. В рамках этого проекта уже имеются условия для проведения торгов и в настоящее время проводятся открытые торги.
II. ОБЩИЙ ОБЗОР ПРОЕКТОВ И ОГРАНИЧЕНИЙ
Проект"Ядерная энергетика", Китай, Хиросима, планирует построить 6 атомных реакторов на миллион кВт, использующих технологию трех поколений
Группа (в том числе два проекта) расположена в городе Хуанъюань, округ Уидон, штат Вайтун.
Контент и сфера охвата: данный тендерный проект разделен на 1 секцию, в рамках которой в Центре АЭС"Тяньцзинь"предлагается электрическая установка
Закупка, установка и ввод в эксплуатацию, основная техническая информация и требования подробно излагаются в Техническом регламенте закупок в рамках проекта. Закупка оборудования для проекта
К ним относятся:
Педагогические системы, конференционные системы, системы педагогической поддержки, системы мультимедиа в классных комнатах и т.д.
Конкретная сфера охвата и требования о проведении торгов зависят от тендерной документации.
Дата поставки и установки:
(1) (1) Установка и отладка всего оборудования (кроме многомедийной системы в классных комнатах) в течение трех месяцев после подписания контракта
Завершается работа системы мультимедиа в классных комнатах в течение шести месяцев после подписания контракта.
2) Участники торгов обеспечивают, чтобы все оборудование было выпущено в течение 180 дней до официального дня поставки. Срок хранения всего оборудования составляет 3 года,
Вступление в силу предварительной приемки и проверки документов, отвечающих требованиям (первоначальная приемка: индикатор технической проверки, в соответствии с которым контрактное оборудование достигается путем проверки
После этого продавец завершил всю работу по договору, которая была принята покупателем. Технические спецификации, конкретно относящиеся к тендерной документации, и основные
В зависимости от того же положения. В течение срока гарантии устройства предоставляется бесплатное послепродажное обслуживание в течение трех лет.

result:
contract_id: CGN-202204240004-N2
contrtact_short_summary: Закупке электрооборудования. Атомная энергетика.
contract_start_date: n/a
contract_deadline_date: n/a
contract_geo: Хуанъюань, округ Уидон, штат Вайтун
tag_construction: 0
tag_energy_not_nuclear: 0
tag_nuclear power: 1
tag_electronics_supply_installation: 1
tag_materials_supplies: 0
tag_equipment_supply_installation: 0
tag_research_design_works: 0
tag_chemical_production: 0
tag_other_services: 0


input:

"""

base_prompt_meta = """
This is an information block containing data about the contract. Your goal: to analyze and structure information in the form of:
Contract date:
Contract ID: (starting with CGN-)
Subject: (purchased product or service)
Name of the participating company:
Price: (if specified, with units indicated, else RMB)
Customer company:
Bidding Agent:

Examples of a job well done:

input:
Дата выхода: 2023-04-11
Установлены результаты первого из трех башен в морской ветряной трубе на острове Янцзы
(Контингент: CGN-20180529004)
Первый три башни проекта морской ветровой энергетики на Кананге, Китай, и Яньцзян (заявление No CGN-20180529004)
Установлено следующее:
1. Информация о кандидатах:
Hongong Kong
Победитель:
Цены: RMB14 068 380.00
II. ДРУГИЕ ОБЯЗАТЕЛЬСТВА:
III. УПРАВЛЕНИЕ ВЕРХОВНОГО КОМИССАРА
.
Наблюдение за осуществлением данного тендерного проекта /
IV. Связи
Заявители:"Чайна инжиниринг лимитед"
Местонахождение:/
Организация: двойная
Телефон: 0755-88616541
Электронная почта: luozhenggang@cgnpc.com.cn
Агент по торгам:"Чайна инжиниринг лимитед"
Местонахождение:/
Организация: Худо
Телефон: 0755-88610728
Электронная почта:huduo@cgnpc.com.cn
Участник торгов или его главный руководитель (руководитель проекта): (подпись)
Участник торгов или его агент: (глава)

result:
Contract date: 2023-04-11
Contract ID: CGN-20180529004
Subject: Первый три башни проекта морской ветровой энергетики на Кананге, Китай, и Яньцзян
Name of the participating company: Hongong Kong
Price: 14068380.00 RMB
Customer company/agent: "Двойная" @luozhenggang ("Чайна инжиниринг лимитед")
Bidding company/agent: "Худо" @huduo ("Чайна инжиниринг лимитед")


input:
Дата выхода: 2022-10-27
Проект LF LOT152A
Циркуляр результатов
Данный проект LOT152A для немощного водородного комбината (номер тендера: CGN-20220908001) для определения медианы проекта
К ним относятся:
1. Информация о кандидатах:
Название проекта: Проект LOT152A Немоторный водородный комплекс
Китайский институт судовой тяжелой промышленности 718
Цены: RMB: 6,402,000.00
II. ДРУГИЕ ОБЯЗАТЕЛЬСТВА:
/
III. УПРАВЛЕНИЕ ВЕРХОВНОГО КОМИССАРА
/
Наблюдение за данной тендерной программой
IV. Связи
Заявители:"Чайна инжиниринг лимитед"
Организация: Маули
Тел.: 0755-84472583
Электронная почта: maolijun@cgnpc.com.cn
Агент по торгам:"Чайна инжиниринг лимитед"
Организация Объединенных Наций: Желание строить
Тел.: 0755-84436467
Электронная почта: zhujiandong@cgnpc.com.cn
Участник торгов или его главный руководитель (руководитель проекта): (подпись)
Участник торгов или его агент: (глава)

result:
Contract date: 2022-10-27
Contract ID: CGN-20220908001
Subject: Проект LOT152A Немоторный водородный комплекс
Name of the participating company: Китайский институт судовой тяжелой промышленности 718
Price: 6402000.00 RMB
Customer company/agent: "Маули" @maolijun ("Чайна инжиниринг лимитед")
Bidding company/agent: "Желание строить" @zhujiandong ("Чайна инжиниринг лимитед")


input:
Дата выхода: 2023-05-10
500 МВт ветроэнергетического проекта 500 МВт в Китае, платформы для подвески, стенограммы ветротехники
(Контингент: CGN-202303160007)
500 МВт ветроэнергетического проекта, платформы для подвешивания и трех сегментов фундаментальной инженерии ветроэнергетики (запрос на проект)
Номер: CGN-20230316007, в котором указаны следующие лица, выигравшие проект:
1. Информация о кандидатах:
Китайская энергетическая корпорация Цзянсу
Цены на юань: рухнули юань
(Слово: CNY 34, 455, 757.00)
II. ДРУГИЕ ОБЯЗАТЕЛЬСТВА:
Нет.
III. УПРАВЛЕНИЕ ВЕРХОВНОГО КОМИССАРА
/.
Наблюдение за данной тендерной программой
IV. Связи
Приглашение:"Чайна Хиросима"
Адрес:
Организация: джентльмен
Тел.: 010-63711535
Электронная почта: guobijun@cgnpc.com
Агент по торгам:"Чайна инжиниринг лимитед"
Адрес:
Организация: Роливер
Тел.: 0755-84437623
Электронная почта: luolihua@cgnpc.com.cn
Участник торгов или его главный руководитель (руководитель проекта): (подпись)
Участник торгов или его агент: (глава)

result:
Contract date: 2023-05-10
Contract ID: CGN-202303160007
Subject: 500 МВт ветроэнергетического проекта, платформы для подвешивания и трех сегментов фундаментальной инженерии ветроэнергетики
Name of the participating company: Китайская энергетическая корпорация Цзянсу
Price: 34455757.00 CNY
Customer company/agent: "Джентльмен" @guobijun ("Чайна Хиросима")
Bidding company/agent: "Роливер" @luolihua ("Чайна инжиниринг лимитед")


input:
Дата выхода: 2023-08-23
Закупка наружного оборудования GIS на базе Синьцзян-2023 (первый пункт: проект ветроэнергетики)
Результаты
(Контингент: CGN-202307040025)
Закупка оборудования GIS на открытом воздухе для проекта Синьцзян-2023 (первый пункт: проект ветроэнергетики)
Номер: CGN-202307040025, идентифицированные лица:
1. Информация о кандидатах:
Santone Tencent
Цены: ¥19 767 203.00
II. ДРУГИЕ ОБЯЗАТЕЛЬСТВА:
Нет
III. УПРАВЛЕНИЕ ВЕРХОВНОГО КОМИССАРА
Надзор за осуществлением данного тендерного проекта /.
IV. Связи
Участники торгов: China and China New Energy Sound
Свяжитель: Белый
Тел.: 010-63711985
Электронная почта: baishaopeng@cgnpc.com.cn
Агент по торгам:"Чайна инжиниринг лимитед"
Контактное лицо: Ли Хун
Тел.: 0755-84436511
Электронная почта:
lhyts@cgnpc.com.cn
Участник торгов или его главный руководитель (руководитель проекта): (подпись)
Участник торгов или его агент: (глава)

result:
Contract date: 2023-08-23
Contract ID: CGN-202307040025
Subject: Закупка наружного оборудования GIS на базе Синьцзян-2023 (первый пункт: проект ветроэнергетики)
Name of the participating company: Santone Tencent
Price: 19767203.00 ¥
Customer company/agent: "Белый" @baishaopeng ("China and China New Energy Sound")
Bidding company/agent: "Ли Хун" @lhyts ("Чайна инжиниринг лимитед")


input:
Дата выхода: 2022-10-24
Закупка (перезакупка) рамочного соглашения по кабелям типа K3 класса 1E на 2022-2024 годы (CGN-20220704001-N1
Циркуляр результатов
В рамках этого проекта были отобраны следующие кандидаты:
I. Информация о участниках:
Название проекта: Закупка рамочного соглашения по кабелям типа K3 класса 1E в 2022-2024 годах (перезакупка)
Производитель: Hong Kong Company
Цена: юань крутится
(Слово: CNY 21,002, 422.00)
Другие объявления: /
III. УПРАВЛЕНИЕ ВЕРХОВНОГО КОМИССАРА
Наблюдение за осуществлением данного тендерного проекта
IV. Связи
Заявители:"Хинли инжиниринг инжиниринг", Пекин
СОДЕРЖАНИЕ (продолжение)
Телефон: 010-82467001
Электронная почта: ZhangQuan2@cgnpc.com.cn
Агент по торгам:"Чайна инжиниринг лимитед"
СОДЕРЖАНИЕ (продолжение)
Тел.: 0755-84436526
Электронная почта: dongdianhe@cgnpc.com.cn
Участник торгов или его главный руководитель (руководитель проекта): (подпись)
Участник торгов или его агент: (глава)

result:
Contract date: 2022-10-24
Contract ID: CGN-20220704001-N1
Subject: Закупка рамочного соглашения по кабелям типа K3 класса 1E в 2022-2024 годах (перезакупка)
Name of the participating company: Hong Kong Company
Price: 21002422.00 CNY
Customer company/agent: "Хинли инжиниринг инжиниринг" @ZhangQuan2 ("Хинли инжиниринг инжиниринг")
Bidding company/agent: "Чайна инжиниринг лимитед" @dongdianhe ("Чайна инжиниринг лимитед")

input:

"""