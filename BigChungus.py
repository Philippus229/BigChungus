import discord, os, random, time, shutil
from tkinter import *
from tkinter import messagebox
from multiprocessing import Process

client = discord.Client()

def get_rand(categories, rating):
    if rating == "all":
        randrating = random.randint(0, 1)
        rating = "sfw" if randrating == 0 else "nsfw"
    category = categories[random.randint(0, len(categories)-1)]
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    imagedir = os.path.join(os.path.join(scriptdir, rating), category)
    filelist = os.listdir(imagedir)
    return os.path.join(imagedir, filelist[random.randint(0, len(filelist)-1)])

categories = [x.replace("\n", "").lower() for x in open("categories.cfg", "r").readlines()]
botmode = open("mode.cfg", "r").readlines()[0].replace("\n", "").lower().split(":")
saved_channel = int(open("saved_channel.cfg", "r").read())

def get_allowed_categories():
    return categories if botmode[1] == "all" else botmode[1].split(";")

@client.event
async def on_ready():
    print(f"Connected to bot ({client.user})...")
    if botmode[0] == "auto":
        timerthing = open("mode.cfg", "r").readlines()[1].replace("\n", "").lower().split(":")
        timermode = timerthing[0]
        times = [float(x) for x in timerthing[1].split(";")]
        await auto_activity(timermode, times, True)
        while True:
            await auto_activity(timermode, times, False)
    
@client.event
async def on_message(message):
    if len(message.content) > 0:
        if message.content[0] == '!':
            newmsg = message.content.lower().replace("!", "").split(":")
            if newmsg[0] in categories or newmsg[0] == "all":
                if newmsg[0] in get_allowed_categories() or botmode[1] == "all":
                    if newmsg[1] == botmode[2] or botmode[2] == "all":
                        file = get_rand(get_allowed_categories(), newmsg[1]) if newmsg[0] == "all" else get_rand([newmsg[0]], newmsg[1])
                        namesplit = file.split(".")
                        await message.channel.send(file=discord.File(file, f"0.{namesplit[len(namesplit)-1]}"))
                    else:
                        await message.channel.send(f"You're not allowed to access {newmsg[1]} content!")
                else:
                    if newmsg[1] == "all":
                        await message.channel.send("You don't have access to all categories!")
                    else:
                        await message.channel.send("You're not allowed to access this category!")
            elif newmsg[0] == "here":
                open("saved_channel.cfg", "w").write(str(message.channel.id))
            else:
                await message.channel.send("This category doesn't exist!")

async def auto_activity(timermode, times, isfirstloop):
    if isfirstloop:
        time.sleep(5)
        print("Timer initialized...")
    timeout = random.randint(times[0]*60, times[1]*60) if timermode == "random" else times[0]*60
    time.sleep(timeout)
    file = get_rand(get_allowed_categories(), botmode[2])
    namesplit = file.split(".")
    await client.get_channel(saved_channel).send(file=discord.File(file, f"0.{namesplit[len(namesplit)-1]}"))

class CategoryDialog:
    def __init__(self, master, bCG):
        self.bCG = bCG
        self.newmaster = Toplevel(master)
        self.newmaster.title("Add category")
        self.catNameLabel = Label(self.newmaster, text="Category:")
        self.catNameLabel.grid(row=0, column=0, sticky=W)
        self.catName = Entry(self.newmaster)
        self.catName.grid(row=1, column=0, sticky=W)
        self.okButton = Button(self.newmaster, text="OK", command=self.addCat)
        self.okButton.grid(row=2, column=0, sticky=W)
        self.cancelButton = Button(self.newmaster, text="Cancel", command=self.close)
        self.cancelButton.grid(row=2, column=1, sticky=W)

    def addCat(self):
        if len(self.catName.get()) > 0 and not self.catName.get().lower() in self.bCG.catlist:
            self.bCG.categoriesList.insert(END, self.catName.get().lower())
            self.bCG.catlist.append(self.catName.get().lower())
        self.close()

    def close(self):
        self.newmaster.destroy()

class AutoDialog:
    def __init__(self, master, bCG):
        self.bCG = bCG
        self.newmaster = Toplevel(master)
        self.newmaster.title("Automatic Mode")
        self.isRandomCheck = Checkbutton(self.newmaster, text="Random?", variable=self.bCG.isRandom)
        self.isRandomCheck.grid(row=0, column=0, sticky=W)
        self.delay = Entry(self.newmaster)
        self.delay.grid(row=1, column=0, sticky=W)
        self.okButton = Button(self.newmaster, text="OK", command=self.ok)
        self.okButton.grid(row=2, column=0, sticky=W)
        self.cancelButton = Button(self.newmaster, text="Cancel", command=self.close)
        self.cancelButton.grid(row=2, column=1, sticky=W)

    def ok(self):
        if len(self.delay.get()) > 0:
            self.bCG.time = self.delay.get()
        self.close()

    def close(self):
        self.newmaster.destroy()

class SettingsWindow:
    def __init__(self, master):
        self.newmaster = Toplevel(master)
        self.newmaster.title("Settings")
        self.catlist = []
        self.isSFW = BooleanVar(self.newmaster, False, "isSFW")
        self.isNSFW = BooleanVar(self.newmaster, False, "isNSFW")
        self.isAuto = False
        self.isRandom = BooleanVar(self.newmaster, False, "isRandom")
        self.time = ""
        self.categoriesLabel = Label(self.newmaster, text="Categories:")
        self.categoriesLabel.grid(row=0, column=0, sticky=W)
        self.categoriesList = Listbox(self.newmaster)
        self.categoriesList.grid(row=1, column=0, sticky=W)
        self.addCategoryButton = Button(self.newmaster, text="+", command=self.addCategoryDialog)
        self.addCategoryButton.grid(row=1, column=1, sticky=W)
        self.removeCategoryButton = Button(self.newmaster, text="-", command=self.removeCategory)
        self.removeCategoryButton.grid(row=1, column=2, sticky=W)
        self.botModeLabel = Label(self.newmaster, text="Bot mode:")
        self.botModeLabel.grid(row=2, column=0, sticky=W)
        self.botModeManual = Button(self.newmaster, text="Manual", command=self.manual)
        self.botModeManual.grid(row=3, column=0, sticky=W)
        self.botModeAuto = Button(self.newmaster, text="Auto", command=self.auto)
        self.botModeAuto.grid(row=3, column=1, sticky=W)
        self.ratingsLabel = Label(self.newmaster, text="Allowed ratings:")
        self.ratingsLabel.grid(row=4, column=0, sticky=W)
        self.ratingSFW = Checkbutton(self.newmaster, text="SFW", variable=self.isSFW)
        self.ratingSFW.grid(row=5, column=0, sticky=W)
        self.ratingNSFW = Checkbutton(self.newmaster, text="NSFW", variable=self.isNSFW)
        self.ratingNSFW.grid(row=5, column=1, sticky=W)
        self.save_button = Button(self.newmaster, text="Save", command=self.save)
        self.save_button.grid(row=6, column=0, sticky=W)
        self.save_button = Button(self.newmaster, text="Close", command=self.close)
        self.save_button.grid(row=6, column=1, sticky=W)
        self.load()

    def addCategoryDialog(self):
        catDialog = CategoryDialog(self.newmaster, self)

    def removeCategory(self):
        for cat in self.categoriesList.curselection():
            self.catlist.remove(self.categoriesList.get(cat))
            self.categoriesList.delete(cat)

    def manual(self):
        self.isAuto = False

    def auto(self):
        self.isAuto = True
        autoDialog = AutoDialog(self.newmaster, self)
        
    def save(self):
        with open("categories.cfg", "w") as f:
            for cat in self.catlist:
                f.write(cat)
                if cat != self.catlist[len(self.catlist)-1]:
                    f.write("\n")
            f.close()
        with open("mode.cfg", "w") as f:
            if self.isAuto:
                f.write("auto:")
            else:
                f.write("manual:")
            f.write("all:") #TODO: Make category selection thing
            if self.isSFW.get() and self.isNSFW.get():
                f.write("all")
            elif self.isNSFW.get():
                f.write("nsfw")
            else:
                f.write("sfw")
            if self.isAuto:
                if self.isRandom.get():
                    f.write("\nrandom:")
                else:
                    f.write("\nnormal:")
                f.write(self.time)
            f.close()
        for folder in os.listdir("sfw"):
            if not folder in self.catlist:
                shutil.rmtree(os.path.join("sfw", folder))
        for folder in os.listdir("nsfw"):
            if not folder in self.catlist:
                shutil.rmtree(os.path.join("nsfw", folder))
        for category in self.catlist:
            if not os.path.isdir(os.path.join("sfw", category)):
                os.mkdir(os.path.join("sfw", category))
            if not os.path.isdir(os.path.join("nsfw", category)):
                os.mkdir(os.path.join("nsfw", category))
        messagebox.showinfo("Saved!", "The configuration was saved!")
        self.close()

    def close(self):
        self.newmaster.destroy()

    def load(self):
        for category in [line.replace("\n", "") for line in open("categories.cfg", "r").readlines()]:
            self.categoriesList.insert(END, category)
            self.catlist.append(category)
        config = [line.lower().replace("\n", "").split(":") for line in open("mode.cfg").readlines()]
        if config[0][0] == "auto":
            self.isAuto = True
        else:
            self.isAuto = False
        if config[0][2] == "all":
            self.isSFW.set(True)
            self.isNSFW.set(True)
        elif config[0][2] == "nsfw":
            self.isNSFW.set(True)
            self.isSFW.set(False)
        else:
            self.isSFW.set(True)
            self.isNSFW.set(False)
        if len(config) > 1:
            if config[1][0] == "random":
                self.isRandom.set(True)
            else:
                self.isRandom.set(False)
            self.time = config[1][1]
        
class BigChungus:
    def __init__(self, master):
        self.master = master
        self.settingsButton = Button(master, text="Settings", command=self.settings)
        self.settingsButton.grid(row=0, column=0, sticky=W)

    def settings(self):
        settingsWindow = SettingsWindow(self.master)

def runGUI():
    root = Tk()
    bigChungus = BigChungus(root)
    root.mainloop()

if __name__=='__main__':
    p0 = Process(target=runGUI)
    p0.start()
    client.run("<bot_token_goes_here>")
