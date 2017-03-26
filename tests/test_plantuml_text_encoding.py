from htmlvis import plantuml_text_encoding


def test_encode_a_simple_diagram():
    diagram = '''
    Alice -> Bob : hello
    Bob -> Alice : world
    '''
    expected = 'ur800iUSpEHK1Lqx1QVy90KhXOpKd9nyBf04Y0yKXiXRAPJd5-MaW2K0'
    assert plantuml_text_encoding.encode(diagram) == expected


def test_basic_example():
    diagram = '''
    Alice -> Bob: Authentication Request
    Bob --> Alice: Authentication Response

    Alice -> Bob: Another authentication Request
    Alice <-- Bob: another authentication Response
    '''
    expected = 'ur800iUSpEHK1Lqx1QVy92i5nzAIZDIyaipan9BC_3o5eDJ2qjJY4YwGGg2yWYvG7LW35fN51VbvnQbSN5WCpSi7gYrIICHjE4I3ZQukH4SYBXrGIq1Q0000'
    assert plantuml_text_encoding.encode(diagram) == expected


def test_declaring_participant():
    diagram = '''
    actor Foo1
    boundary Foo2
    control Foo3
    entity Foo4
    database Foo5
    Foo1 -> Foo2 : To boundary
    Foo1 -> Foo3 : To control
    Foo1 -> Foo4 : To entity
    Foo1 -> Foo5 : To database
    '''
    expected = 'ur80WiJaalmY1RVyV4Ck43SflpGl9R6e4YHY11P9piyhAShF0GaOWmLIyqeoIy0AJC3ybCIInAJ4ubIGY2bO16IQWguTs0m5AuMGVBYnwDB646ce7UYo9X1PY8NeagOGIPZjO6a0'
    assert plantuml_text_encoding.encode(diagram) == expected


def test_colored_participant():
    diagram = r'''
    actor Bob #red
    ' The only difference between actor
    'and participant is the drawing
    participant Alice
    participant "I have a really\nlong name" as L #99FF99
    /' You can also declare:
       participant L as "I have a really\nlong name"  #99FF99
      '/

    Alice->Bob: Authentication Request
    Bob->Alice: Authentication Response
    Bob->L: Log transaction
    '''
    expected = 'VP0nRm8n38Nt-nLFC30Xvhi1YGv8bMv2NIfrCOav8gNsDSaLyUzhmW1j4Puil-yzsMvWHQvemelkCK_icyjeWRSZGoMUuSFXm8d5CVPSJinoDLmv4e-HKWakZ2G58QEOqoSw1HagSozlOd3yRpfxnP6-6OJ45EFvGwBA0A5Fde4oUipRThjjs-fSBV2k4npP8Z4hFBj8YRig_adkB_QdyR-YxQ1LKxkww79jJ-cmcUmaiKmgGGKx_feubugPlbnNzW6MHvNCDwxlqEk0aaYolT2Wglq0'
    assert plantuml_text_encoding.encode(diagram) == expected


def test_use_non_letter_in_participants():
    diagram = r'''
    Alice -> "Bob()" : Hello
    "Bob()" -> "This is very\nlong" as Long
    ' You can also declare:
    ' "Bob()" -> Long as "This is very\nlong"
    Long --> "Bob()" : ok
    '''
    expected = 'ur800iUSpEHK1Lqx1IMd_2GDJIK5AmMFr9oSV2wG94mC91sIaLci04HbgKMLCNav-NdfIWg9nGe-G0POhRf2P7wfGd9Yda9YJd6-GafgSavYKQeLL0x9990Ea4vi9e9LWnNeeZWfFnii0m00'
    assert plantuml_text_encoding.encode(diagram) == expected


def test_message_to_self():
    diagram = r'''
    Alice->Alice: This is a signal to self.\nIt also demonstrates\nmultiline \ntext
    '''
    expected = '7Omn2e1030JxUyL-G1zW8LZQMruJD6eWbmCJmUTxEWnCDmcDIMNbRlmpO3d5qIIu74QAg73MlSys1qYzOkDIpUEYOCzMRWrHCKQsu2VIztm1'
    assert plantuml_text_encoding.encode(diagram) == expected


def test_change_arrow_style():
    diagram = r'''
    Bob ->x Alice
    Bob -> Alice
    Bob ->> Alice
    Bob -\ Alice
    Bob \\- Alice
    Bob //-- Alice

    Bob ->o Alice
    Bob o\\-- Alice

    Bob <-> Alice
    Bob <->o Alice
    '''
    expected = 'ur800gVy90LTkme5nvpCv5GkX0Y608P839f0J8mkceY-lYvC2CcWV3HL-K2D6CfiC5nWWweJ0000'
    assert plantuml_text_encoding.encode(diagram) == expected


def test_change_arrow_color():
    diagram = r'''
    Bob -[#red]> Alice : hello
    Alice -[#0000FF]->Bob : ok
    '''
    expected = 'ur800gVy90NTQEMYr9HOEmN7dCpaL0KhXOpKd9nyBf0qH0Iem008tDnYTUr06gmKyhF1qW00'
    assert plantuml_text_encoding.encode(diagram) == expected


def test_message_sequence_numbering():
    diagram = r'''
    autonumber
    Bob -> Alice : Authentication Request
    Bob <- Alice : Authentication Response
    '''
    expected = 'ur80WiJIaloyqjoar28k4DSfFqb1rqx1CISpELN1Ii6nj2GZDQyaCpcn93C_Jo4ejR0qjRW4hj965xVAueBylE9Ki580'
    assert plantuml_text_encoding.encode(diagram) == expected


def test_format_with_html_tags():
    diagram = r'''
    autonumber "<b>[000]"
    Bob -> Alice : Authentication Request
    Bob <- Alice : Authentication Response

    autonumber 15 "<b>(<u>##</u>)"
    Bob -> Alice : Another authentication Request
    Bob <- Alice : Another authentication Response

    autonumber 40 10 "<font color=red><b>Message 0  "
    Bob -> Alice : Yet another authentication Request
    Bob <- Alice : Yet another authentication Response
    '''
    expected = 'bOun2y8m48Nt_8gZNNGefg2Bn43TNTn47D9wQg7cDBdyVnCH1sb4RxttlVS9Y6S2amtN5XqKgjLxAUMX4EcpfXOg3StGTmXBQ09Vq7BV6Ux9mXRl0Js_awhA9_sDh4SXFlRgnNDoee8kIpKBUZe-R2dskKJ-Af0ZCY9p2RMCBYUo31qDv5OEZpgwRT1xSqQG0ADkEsGmV_jzfLwE2Ni0'
    assert plantuml_text_encoding.encode(diagram) == expected


def test_split_diagrams():
    diagram = r'''
    Alice -> Bob : message 1
    Alice -> Bob : message 2

    newpage

    Alice -> Bob : message 3
    Alice -> Bob : message 4

    newpage A title for the\nlast page

    Alice -> Bob : message 5
    Alice -> Bob : message 6
    '''
    expected = 'ur800iUSpEHK1Lqx1QVy90KhXTpKukB4z5G5GouyaaPSODcyrF8289SBdr9ZV98cAEOeE2gKP9Raf2gavHSfb6IankJb91QNA12qmXIVf1bO4W00'
    assert plantuml_text_encoding.encode(diagram) == expected


def test_grouping_messages():
    diagram = r'''
    Alice -> Bob: Authentication Request

    alt successful case

        Bob -> Alice: Authentication Accepted

    else some kind of failure

        Bob -> Alice: Authentication Failure
        group My own label
            Alice -> Log : Log attack start
            loop 1000 times
                Alice -> Bob: DNS Attack
            end
            Alice -> Log : Log attack end
        end

    else Another type of failure

       Bob -> Alice: Please repeat

    end
    '''
    expected = 'ZP51RW8n34NtSuf_WKh3baMbe8fLYr1xWf3nq8WGfx6ZYjkJ6Q1jH1Tu4KNwpr_sTuTQ9dX7U7h6YdTBcAAV5DKxgvuZtkcha6ZNJQGD2YdEaSXO0fmLkWXJrUx9P7Qxip6rAIaD5vo248IFX8EF0tZ4Q7qe-L6tzPM-mVlC9U7j1FwE27P7uKTg5dpbFPRpQrMjEq3KPctOm9omwFiUweyaZNOVrilc0sQsQa2AmuC3_2Md_syy9dBTEKDFYVvBg0re6wWU0vaIsUknRjPd'
    assert plantuml_text_encoding.encode(diagram) == expected


def test_notes_on_diagrams():
    diagram = r'''
    Alice->Bob : hello
    note left: this is a first note

    Bob->Alice : ok
    note right: this is another note

    Bob->Bob : I am thinking
    note left
        a note
        can also be defined
        on several lines
    end note
    '''
    expected = 'NOr13eCm30JlUSL-W0zmG6flVKOWXbYuZfH4VN-T84hRbI_UtR4TJ3VXXORfdcQCY2IINBCrLOBGMaVKo0Ks7YldKdlaUicWOUe7Z4tx1MRUuZTfPgJyJnu_7_3FrjITTVlztRScVw3dkdY5bv8m4mAjh1G-ML8KUb7s0h6Wz80qN1VU'
    assert plantuml_text_encoding.encode(diagram) == expected


def test_notes_relative_to_participants():
    diagram = r'''
    participant Alice
    participant Bob
    note left of Alice #aqua
        This is displayed
        left of Alice.
    end note

    note right of Alice: This is displayed right of Alice.

    note over Alice: This is displayed over Alice.

    note over Alice, Bob #FFAAAA: This is displayed\n over Bob and Alice.

    note over Bob, Alice
        This is yet another
        example of
        a long note.
    end note
    '''
    expected = 'TL1B3eCW4DrpYadS6W_GdLruWYwxcUeW91GeqgRUlWCcIgrzOSFx1Pu0XiSGTQyzsWYjqJs9FNjsjynP5maCoGXEBbQeyF74B2PSb9w0pw0dRt2cOLM-KascoGwvKMpTGOzgivr--tQEfiYw5uN_kKqzpjJfar1rNSiuABZQnPnSo0y_hcArBZOi9vafSj15HM7Lw8rtRpWhLmh1E3lcojrAwV81'
    assert plantuml_text_encoding.encode(diagram) == expected


def test_changing_note_shape():
    diagram = r'''
    caller -> server : conReq
    hnote over caller : idle
    caller <- server : conConf
    rnote over server
     "r" as rectangle
     "h" as hexagon
    endrnote
    '''
    expected = 'LOn12e0m30JlVSNIUpyWuiKV-8DIenLAWb74vwjHK7DAPZFhS4wAfP0YD5X8jtEha8GxcjsLPfQL81T_7YjCVI7tKUlmKrlXmM9ztJit2gyUSO5IMYEFJnLyDfffZwEmCUBUAkmu0000'
    assert plantuml_text_encoding.encode(diagram) == expected


def test_creole_and_html():
    diagram = r'''
    participant Alice
    participant "The **Famous** Bob" as Bob

    Alice -> Bob : hello --there--
    ... Some ~~long delay~~ ...
    Bob -> Alice : ok
    note left
      This is **bold**
      This is //italics//
      This is ""monospaced""
      This is --stroked--
      This is __underlined__
      This is ~~waved~~
    end note

    Alice -> Bob : A //well formatted// message
    note right of Alice
     This is <back:cadetblue><size:18>displayed</size></back>
     __left of__ Alice.
    end note
    note left of Bob
     <u:red>This</u> is <color #118888>displayed</color>
     **<color purple>left of</color> <s:red>Alice</strike> Bob**.
    end note
    note over Alice, Bob
     <w:#FF33FF>This is hosted</w> by <img sourceforge.jpg>
    end note
    '''
    expected = 'TL71JeGm5BplLxpWhH6QZHT3I1Czy0Dw9uM-XRg5HzhYHWzyksrtrHMr8I7Cl3SpJ7SGpYojrvsUvUJXmUWETriqUnuG6AlbI8jZ31wfpK2w-DwbuRG6kOW8b32WCGHvxWUqcETff2WAUA8HOLqDJJqeDF9jNIEU-BWP1CvA9T0neHDv18C7dxu0dWVj83oCjMGKOnkOS-rbK72SRvWi6saYDyiELPPjo3nttj8HrINhDzCqowJG6ZsXQfeDkQud-OfgNHEEaqfn_spa8KGxXLRWG7QKtgFY74PqJlRu_QDMzuC7EbnTmvTPrShkM7PIeM_DWg9o-XtB_RrGsisXIbGLZv2eU9mKv-scYUK5oQOvYnO_i_xeE3h7AqsRrL9QL2BQLtmHAK97XYpSxFVtuLmR9-9YoTXbRbxiR51Sb3-7e799EAK9aRtLHqmrCVPVE7f5Uuv_UnNmLDxKzTrTNOlFZWPoFiOv2MZVeD9Z3uuMss5elSVYPUx5RuSF'
    assert plantuml_text_encoding.encode(diagram) == expected


def test_divider():
    diagram = r'''
    == Initialization ==

    Alice -> Bob: Authentication Request
    Bob --> Alice: Authentication Response

    == Repetition ==

    Alice -> Bob: Another authentication Request
    Alice <-- Bob: another authentication Response
    '''
    expected = 'VOsn3O0m30JxJE45iW0YID3Hia68B64fSe2OXkbn22NWqd_tRq3FEHYPX7oaqmibreyn9UaZ1GJRmP3c1lf35cIXKA49jmEptA3cO9MxXHSohuaprbATct15eRyfJjgmW_-Uh49hRJNyb_5C5-K2'
    assert plantuml_text_encoding.encode(diagram) == expected


def test_reference():
    diagram = r'''
    participant Alice
    actor Bob

    ref over Alice, Bob : init

    Alice -> Bob : hello

    ref over Bob
      This can be on
      several lines
    end ref
    '''
    expected = 'NOox3SCm34HxJN4390ka213Fa0LecO484AGX2PdV5gtALv7lFWcdTgfTikna7H-Lp6bGojqh5bzJl9L_y3_NA_4O1buGatxvWV5yJwEmgj-QOmkXRv66J8QLuJPXupD42XNZ5enj6-su3m00'
    assert plantuml_text_encoding.encode(diagram) == expected


def test_delay():
    diagram = r'''
    Alice -> Bob: Authentication Request
    ...
    Bob --> Alice: Authentication Response
    ...5 minutes latter...
    Bob --> Alice: Bye !
    '''
    expected = 'ur800iUSpEHK1Lqx1QVy92i5nzAIZDIyaipan9BC_3o5eDJ2qjJY4YwGGZqzFJ0DLAUW2rGFreX5Ht51VbvnAaoBgK9kPbvfIMgnGavYIKbg4GvJd2fJ5HJ14W00'
    assert plantuml_text_encoding.encode(diagram) == expected


def test_space():
    diagram = r'''
    Alice -> Bob: message 1
    Bob --> Alice: ok
    |||
    Alice -> Bob: message 2
    Bob --> Alice: ok
    ||45||
    Alice -> Bob: message 3
    Bob --> Alice: ok
    '''
    expected = 'ur800iUSpEHK1Lqx1QVy92k5tDJYuiJqL0L3Bf0SK4X15oW5LcEba9yD5gsfgU72hTC8hquJKxoQZV5e1W00'
    assert plantuml_text_encoding.encode(diagram) == expected


def test_lifeline_activation_and_destruction():
    diagram = r'''
    participant User

    User -> A: DoWork
    activate A

    A -> B: << createRequest >>
    activate B

    B -> C: DoWork
    activate C
    C --> B: WorkDone
    destroy C

    B --> A: RequestCreated
    deactivate B

    A -> User: Done
    deactivate A
    '''
    expected = 'ROz12iCW44Ntdc8ka0k48AWvGQ5qBMOMKeZfP5hexUkCIMb3NEdtyVwCWNgMI9nJNkBCS5sHZ95KRj1PS3sCvLRehcbCd5-H4LoZd22-Xs60H5W_BlXuuifWxJ_l6--53-VAeCy0NLCAC9OPDPsgaygxChkcZRRL1UsUDlHOgaFAFjBx5Vwi8i47'
    assert plantuml_text_encoding.encode(diagram) == expected
