from modules import loading

loading.loading();

run = True

while run:
    if loading.run() == False:
        run = False