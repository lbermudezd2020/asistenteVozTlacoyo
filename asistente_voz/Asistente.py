import pyttsx3 #convierte el texto introducido en voz
import datetime
import speech_recognition as sr #Biblioteca para realizar reconocimiento de voz
import wikipedia # biblioteca de Python que facilita el acceso y el análisis de datos de Wikipedia
import webbrowser as wb
import psutil #biblioteca multiplataforma para recuperar información sobre procesos
import smtplib #define un objeto de sesión de cliente SMTP que se puede usar para enviar correo
from email.message import EmailMessage
import pywhatkit # automatización de WhatsApp y YouTube
from twilio.rest import Client
import cv2 #opencv
import numpy as np # utilizar como un contenedor multidimensional


engine = pyttsx3.init() #convierte el texto introducido en voz
voices = engine.getProperty('voices') #
engine.setProperty('voice', voices[0].id)
newVoiceRate = 200 #el nivel de lentitud
engine.setProperty('rate', newVoiceRate)
cap = cv2.VideoCapture(0)
faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#funcion para hablar 
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#funcion para tomar el tiempo y transformar
def time():
    time = datetime.datetime.now().strftime('%I:%M')
    speak('Son las')
    speak(time)

#funciom en que qle que nos dice el dia, mes y año
def date():
    year = int(datetime.datetime.now().year) #representar la fecha y la hora en formatos
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    speak('Estamos al dia')
    speak(day)
    speak('Del mes')
    speak(month)
    speak('Del año')
    speak(year)

#funcion para inciar
def saludo():
    speak("Bienvenido al Praxthon, como esta?")
    tiempo = datetime.datetime.now().hour 
    if tiempo >= 6 and tiempo < 12: #se valida dependiendo de la hora del dia
        speak("Buenos Dias")
    if tiempo >= 12 and tiempo < 18:
        speak("Buenas Tardes")
    if tiempo >= 18 and tiempo < 24:
        speak("Buenas Noches")
    speak("Tu asistente Tlacoyo al servicio, Como puedo ayudarte?")

#esto es para darle tiempo que escuche
def orden():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Escuchando...')
        r.pause_threshold = 1 #se detiene para poder escuchar
        audio = r.listen(source)
    try:
        print('Reconociendo...')
        query = r.recognize_google(audio, language='es-ES') #para español Mexico
    except Exception as e:
        print(e)
        speak('Repetir por favor')
        return 'None'
    return query

#nos da la informacion del sistema
def EstadoDelSistema():
    uso_de_cpu = str(psutil.cpu_percent())#recuperar información sobre procesos del so
    frequencia_de_cpu = str(psutil.cpu_freq())
    speak("El uso de CPU es de" + uso_de_cpu)
    speak("La frequencia del procesador es" + frequencia_de_cpu)

#funcion para enviar el emial
def Enviaremail(para):#recibe el para aq uien va dirijido desde la consola
    email_subject = "Asistente de voz desde Python"
    sender_email_address = "lbermudezd001@gmail.com"
    receiver_email_address = para
    email_smtp = "smtp.gmail.com"
    email_password = "xvlqurjbcqqnyxsf"

    contenido = EmailMessage() #se crea un objeto y le pasamos todo lo del email
    contenido['Subject'] = email_subject
    contenido['From'] = sender_email_address
    contenido['To'] = receiver_email_address
    contenido.set_content("https://www.youtube.com/watch?v=SH8lOOk1OG8")

    server = smtplib.SMTP(email_smtp, '587') #servidor de correo SMTP y el número de puerto.
    server.ehlo()#identifica el cliente de correo
    server.starttls() #conexión TLS segura al servidor usando starttls()
    server.login(sender_email_address, email_password)#le pasamos los datos 
    server.send_message(contenido)
    server.quit()


def Objetos():
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #opencv se utiliza para todo la deteccion 
        canny = cv2.Canny(gray, 10, 150)
        canny = cv2.dilate(canny, None, iterations=1)
        canny = cv2.erode(canny, None, iterations=1)
        cnts, _ = cv2.findContours(
            canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        obj = faceClassif.detectMultiScale(gray,
                                           scaleFactor=1.1,
                                           minNeighbors=5,
                                           minSize=(30, 30),
                                           maxSize=(200, 200))

        for (x, y, w, h) in obj:
           # epsilon = 0.01*cv2.arcLength(c,True)
            #approx = cv2.approxPolyDP(x,epsilon,True)

            #x,y,w,h = cv2.boundingRect(approx)

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


# Menu principal
if __name__ == '__main__':
    saludo()
    while True:
        query = orden().lower() #esto es para hacer minusculas con lower
        print(query)
        if 'hora' in query:
            time()
        elif 'dia' in query:
            date()
        elif 'salir' in query:
            speak('Gracias fue un gusto hablar contigo, nos vemos')
            quit()
        elif 'wikipedia' in query: #se inicia y nos dice la fecha y hora actual
            speak('Entendido...')
            query = query.replace('wikipedia', '')
            wikipedia.set_lang('es')#se le asigna el idioma
            result = wikipedia.summary(query, sentences=2) #Esta función recupera el resumen de una página de Wikipedia sobre un tema en particular
            speak(result)
        elif 'google' in query:
            speak('Abriendo google translate')
            wb.open('https://translate.google.com.mx/?hl=es')
        elif 'linkedin' in query:
            speak('Abriendo linkedin')
            wb.open('https://www.linkedin.com/')
        elif 'amazon' in query:
            speak('Abriendo amazon')
            wb.open('https://www.amazon.com.mx/')
        elif 'youtube' in query:
            speak('abriendo youtube')
            wb.open('https://www.youtube.com/watch?v=SH8lOOk1OG8')
        elif "estado del sistema" in query:
            EstadoDelSistema()
        elif "enviar email" in query:
            try:
                speak("¿Para quien es el correo? escriba el correo en el teclado")
                para = input()
                speak(para)
                speak("Te recomiendo que revises este video de youtube")
                Enviaremail(para)
                speak("El email ah sido enviado")
            except Exception as e:
                print(e)
                speak("Imposible enviar el email")
        elif 'whatsapp' in query:
            try:
                speak("¿Para quien es el whatsapp? escriba el numero en el teclado")
                numeroTel = input()
                speak(numeroTel)
                speak("Te recomiendo que revises este video de youtube")
                numero = "+52"+numeroTel
                mensagem = "https://www.youtube.com/watch?v=SH8lOOk1OG8"
                pywhatkit.sendwhatmsg_instantly(numero, mensagem) #te abre el navegador y te manda el sms y numero
            except Exception as e:
                print(e)
                speak("Imposible enviar whataapp")
        elif 'objetos' in query:
            speak("Detectando objetos")
            Objetos()
            # if 'quitar' in query:
     #   speak('Deteccion de objetos terminada')
      #  quit()
