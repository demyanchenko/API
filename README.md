# Взаимодействие по АПИ

## Статьи
* Хабр. Создание собственного API на Python (FastAPI): Знакомство и первые функции:
https://habr.com/ru/companies/amvera/articles/826196/
* Тпрогер.Как создать API на Python без усилий на деплой 
https://tproger.ru/articles/kak-sozdat-api-na-python-bez-usilij-na-deploj
* Руководство по деплою (во все тяжкие)
https://itandcats.ru/fastapi-deployment-examples

## Хостинг
* Российское облако для хостинга
https://amvera.ru/
* 
# Команды
* Установить библиотеки (зависимости)
pip install -r requirements.txt

* Запуск сервера
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

```plantuml
@startuml
actor User
participant System
User --> System

@enduml
```

```mermaid
C4Context
    title System Context diagram for Internet Banking System
    Workspace(b0, "boundary0") {

%%        !identifiers hierarchical
    
        model {
            u = person "User"
            ss = softwareSystem "Software System" {
                wa = container "Web Application"
                db = container "Database Schema" {
                    tags "Database"
                }
            }
    
            u -> ss "Uses"
            u -> ss.wa "Uses"
            ss.wa -> ss.db "Reads from and writes to"
        }
    
        views {
            systemContext ss "Diagram1" {
                include *
            }
    
            container ss "Diagram2" {
                include *
            }
    
            // styling...
        }
    
    }
```

```mermaid
    C4Context
      title System Context diagram for Internet Banking System
      Enterprise_Boundary(b0, "BankBoundary0") {
        Person(customerA, "Banking Customer A", "A customer of the bank, with personal bank accounts.")
        Person(customerB, "Banking Customer B")
        Person_Ext(customerC, "Banking Customer C", "desc")

        Person(customerD, "Banking Customer D", "A customer of the bank, <br/> with personal bank accounts.")

        System(SystemAA, "Internet Banking System", "Allows customers to view information about their bank accounts, and make payments.")

        Enterprise_Boundary(b1, "BankBoundary") {

          SystemDb_Ext(SystemE, "Mainframe Banking System", "Stores all of the core banking information about customers, accounts, transactions, etc.")

          System_Boundary(b2, "BankBoundary2") {
            System(SystemA, "Banking System A")
            System(SystemB, "Banking System B", "A system of the bank, with personal bank accounts. next line.")
          }

          System_Ext(SystemC, "E-mail system", "The internal Microsoft Exchange e-mail system.")
          SystemDb(SystemD, "Banking System D Database", "A system of the bank, with personal bank accounts.")

          Boundary(b3, "BankBoundary3", "boundary") {
            SystemQueue(SystemF, "Banking System F Queue", "A system of the bank.")
            SystemQueue_Ext(SystemG, "Banking System G Queue", "A system of the bank, with personal bank accounts.")
          }
        }
      }

      BiRel(customerA, SystemAA, "Uses")
      BiRel(SystemAA, SystemE, "Uses")
      Rel(SystemAA, SystemC, "Sends e-mails", "SMTP")
      Rel(SystemC, customerA, "Sends e-mails to")

      UpdateElementStyle(customerA, $fontColor="red", $bgColor="grey", $borderColor="red")
      UpdateRelStyle(customerA, SystemAA, $textColor="blue", $lineColor="blue", $offsetX="5")
      UpdateRelStyle(SystemAA, SystemE, $textColor="blue", $lineColor="blue", $offsetY="-10")
      UpdateRelStyle(SystemAA, SystemC, $textColor="blue", $lineColor="blue", $offsetY="-40", $offsetX="-50")
      UpdateRelStyle(SystemC, customerA, $textColor="red", $lineColor="red", $offsetX="-50", $offsetY="20")

      UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")



```

```mermaid
    C4Container
    title Container diagram for Internet Banking System

    System_Ext(email_system, "E-Mail System", "The internal Microsoft Exchange system", $tags="v1.0")
    Person(customer, Customer, "A customer of the bank, with personal bank accounts", $tags="v1.0")

    Container_Boundary(c1, "Internet Banking") {
        Container(spa, "Single-Page App", "JavaScript, Angular", "Provides all the Internet banking functionality to customers via their web browser")
        Container_Ext(mobile_app, "Mobile App", "C#, Xamarin", "Provides a limited subset of the Internet banking functionality to customers via their mobile device")
        Container(web_app, "Web Application", "Java, Spring MVC", "Delivers the static content and the Internet banking SPA")
        ContainerDb(database, "Database", "SQL Database", "Stores user registration information, hashed auth credentials, access logs, etc.")
        ContainerDb_Ext(backend_api, "API Application", "Java, Docker Container", "Provides Internet banking functionality via API")

    }

    System_Ext(banking_system, "Mainframe Banking System", "Stores all of the core banking information about customers, accounts, transactions, etc.")

    Rel(customer, web_app, "Uses", "HTTPS")
    UpdateRelStyle(customer, web_app, $offsetY="60", $offsetX="90")
    Rel(customer, spa, "Uses", "HTTPS")
    UpdateRelStyle(customer, spa, $offsetY="-40")
    Rel(customer, mobile_app, "Uses")
    UpdateRelStyle(customer, mobile_app, $offsetY="-30")

    Rel(web_app, spa, "Delivers")
    UpdateRelStyle(web_app, spa, $offsetX="130")
    Rel(spa, backend_api, "Uses", "async, JSON/HTTPS")
    Rel(mobile_app, backend_api, "Uses", "async, JSON/HTTPS")
    Rel_Back(database, backend_api, "Reads from and writes to", "sync, JDBC")

    Rel(email_system, customer, "Sends e-mails to")
    UpdateRelStyle(email_system, customer, $offsetX="-45")
    Rel(backend_api, email_system, "Sends e-mails using", "sync, SMTP")
    UpdateRelStyle(backend_api, email_system, $offsetY="-60")
    Rel(backend_api, banking_system, "Uses", "sync/async, XML/HTTPS")
    UpdateRelStyle(backend_api, banking_system, $offsetY="-50", $offsetX="-140")


```
В магазине доступны следующие товары:

| # | Название | Цена | Количество |
|---|----------|------|------------|
| 1 | Adidas | 13.0 ₽ | 2 |
| 2 | Reebok | 9.0 ₽ | 13 |
| 3 | Authlete | 15 ₽ | 1 |
| 4 | Nike shoes | 10.5 ₽ | 1 |
| 5 | Bekka shoes | 15.9 ₽ | 1 |
| 6 | Шмот | 130 ₽ | 1 500 000 |
| 7 | Marvel | 1900 ₽ | 16 |
| 8 | Colin's | 1400 ₽ | 1 |
| 9 | Преображение | 1490 ₽ | 200 |

Всего в магазине **9 наименований** товаров. Если вам что-то приглянулось или нужна дополнительная информация, дайте знать — помогу! 
