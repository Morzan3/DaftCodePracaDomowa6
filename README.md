W zadaniu z flagami zamiast tworzyć 2 bazy danych lepiej utworzyć jedną tabelę ze wspólnymi kolumnami bo o ile się nie
myle tej tabeli nie można bardziej znormalizować. Jeśli można to utworzyć drugą tabelę z tawartości bazy danych
strings i dodać do tabeli countries foregin key na strings id. Zmiany te wydawały mi się jednak zbyt radykalne bo zakładam, że
z jakiegoś powodu te 2 bazy danych zostały utworzone więc nie zmieniałem logiki aplikacji.