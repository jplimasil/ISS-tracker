import json
import turtle
import urllib.request
import webbrowser
import geocoder
import time

# Obter dados sobre os astronautas na ISS
def obter_dados_ISS():
    try:
        url = "http://api.open-notify.org/astros.json"
        response = urllib.request.urlopen(url)
        result = json.loads(response.read())
        with open("iss.txt", "w") as file:
            file.write("Atualmente há " +
                       str(result["number"]) + " astronautas na ISS: \n\n")
            pessoas = result["people"]
            for pessoa in pessoas:
                file.write(pessoa['name'] + " - a bordo" + "\n")
        # Obter coordenadas geográficas atuais
        g = geocoder.ip('me')
        with open("iss.txt", "a") as file:
            file.write("\nSuas coordenadas atuais são: " + str(g.latlng))
    except Exception as e:
        print("Erro ao obter dados da ISS:", e)

# Abrir o arquivo de texto com informações sobre a ISS
def abrir_arquivo_ISS():
    try:
        webbrowser.open("iss.txt")
        time.sleep(2)  # Espera 2 segundos antes de continuar
    except Exception as e:
        print("Erro ao abrir o arquivo ISS:", e)

# Configurar o ambiente do mapa
def configurar_mapa():
    try:
        screen = turtle.Screen()
        screen.setup(1280, 720)
        screen.setworldcoordinates(-180, -90, 180, 90)
        screen.bgpic("midia/map.gif")
        screen.register_shape("midia/iss.gif")
        return screen
    except Exception as e:
        print("Erro ao configurar o mapa:", e)

# Atualizar a posição da ISS no mapa
def atualizar_posicao_ISS():
    try:
        iss = turtle.Turtle()
        iss.shape("midia/iss.gif")
        iss.setheading(45)
        iss.penup()

        # Criar uma caneta para desenhar o rastro
        rastro = turtle.Turtle()
        rastro.penup()
        rastro.color("red")  # Cor do rastro

        while True:
            # Obter a posição atual da ISS
            url = "http://api.open-notify.org/iss-now.json"
            response = urllib.request.urlopen(url)
            result = json.loads(response.read())
            location = result["iss_position"]
            lat = float(location["latitude"])
            lon = float(location["longitude"])

            # Exibir as coordenadas no terminal
            print("\nLatitude: " + str(lat))
            print("Longitude: " + str(lon))

            # Adicionar ponto preto ao rastro
            rastro.goto(lon, lat)
            rastro.dot(2)  # Tamanho do ponto preto

            # Atualizar a posição da ISS no mapa
            iss.goto(lon, lat)

            # Atualizar a cada 5 segundos
            time.sleep(1)
    except Exception as e:
        print("Erro ao atualizar posição da ISS:", e)

# Função principal
def main():
    obter_dados_ISS()
    abrir_arquivo_ISS()
    screen = configurar_mapa()
    if screen:
        atualizar_posicao_ISS()
        screen.mainloop()
        screen.bye()  # Fecha o Turtle ao finalizar

if __name__ == "__main__":
    main()