from .. import loader, utils

@loader.tds
class PersonaBuilder(loader.Module):
    """Создание и управление персонами"""

    strings = {"name": "PersonaBuilder"}

    def __init__(self):
        self.in_progress = {}  # {user_id: {data}}
        self.personas = {}     # {user_id: [persona1, persona2, ...]}

    @loader.command()
    async def создатьп(self, message):
        """Начать создание новой персоны"""
        uid = message.sender_id
        self.in_progress[uid] = {
            "Имя": None,
            "Пол": None,
            "Возраст": None,
            "Что делает": None,
            "Навыки": None
        }
        await message.edit(
            "🆕 Начато создание новой персоны!\n"
            "Доступные команды:\n"
            "• !имя\n• !стать\n• !возвраст\n• !чтоделает\n• !навыки\n• !закончить"
        )

    @loader.command()
    async def имя(self, message):
        """Установить имя персоны: !имя Миша"""
        uid = message.sender_id
        if uid not in self.in_progress:
            return await message.edit("❗ Сначала начни с !создатьп")

        name = utils.get_args_raw(message).strip()
        if not name:
            return await message.edit("❗ Укажи имя, например: !имя Катя")

        self.in_progress[uid]["Имя"] = name
        await message.edit(f"✅ Имя установлено: <b>{name}</b>", parse_mode="html")

    @loader.command()
    async def стать(self, message):
        """Указать пол: !стать девушка/парень"""
        uid = message.sender_id
        if uid not in self.in_progress:
            return await message.edit("❗ Сначала используй !создатьп")

        gender = utils.get_args_raw(message).strip().capitalize()
        if gender not in ["Парень", "Девушка"]:
            return await message.edit("❗ Укажи: парень или девушка")

        self.in_progress[uid]["Пол"] = gender
        await message.edit(f"✅ Пол установлен: {gender}")

    @loader.command()
    async def возвраст(self, message):
        """Установить возраст: !возвраст 18"""
        uid = message.sender_id
        if uid not in self.in_progress:
            return await message.edit("❗ Сначала используй !создатьп")

        age = utils.get_args_raw(message).strip()
        if not age.isdigit():
            return await message.edit("❗ Возраст должен быть числом")

        self.in_progress[uid]["Возраст"] = int(age)
        await message.edit(f"📅 Возраст установлен: {age}")

    @loader.command()
    async def чтоделает(self, message):
        """Описание деятельности: !чтоделает Пишет боты"""
        uid = message.sender_id
        if uid not in self.in_progress:
            return await message.edit("❗ Сначала используй !создатьп")

        text = utils.get_args_raw(message).strip()
        if not text:
            return await message.edit("❗ Укажи описание занятий")

        self.in_progress[uid]["Что делает"] = text
        await message.edit("💼 Деятельность установлена.")

    @loader.command()
    async def навыки(self, message):
        """Список навыков: !навыки Python, харизма"""
        uid = message.sender_id
        if uid not in self.in_progress:
            return await message.edit("❗ Сначала используй !создатьп")

        text = utils.get_args_raw(message).strip()
        if not text:
            return await message.edit("❗ Укажи хотя бы один навык")

        self.in_progress[uid]["Навыки"] = text
        await message.edit("🧠 Навыки установлены.")

    @loader.command()
    async def закончить(self, message):
        """Завершить создание и сохранить"""
        uid = message.sender_id
        if uid not in self.in_progress:
            return await message.edit("❗ Сначала используй !создатьп")

        persona = self.in_progress.pop(uid)
        if None in persona.values():
            return await message.edit("❗ Заполни все поля перед завершением.")

        if uid not in self.personas:
            self.personas[uid] = []

        self.personas[uid].append(persona)

        text = "✅ Персона создана:\n\n"
        for key, value in persona.items():
            text += f"<b>{key}:</b> {value}\n"

        await message.edit(text, parse_mode="html")

    @loader.command()
    async def списокперсон(self, message):
        """Показать всех твоих персон"""
        uid = message.sender_id
        if uid not in self.personas or not self.personas[uid]:
            return await message.edit("📭 У тебя ещё нет персон.")

        text = "<b>📋 Твои персоны:</b>\n\n"
        for i, persona in enumerate(self.personas[uid], start=1):
            text += f"<b>Персона {i}:</b>\n"
            for key, value in persona.items():
                text += f"• <b>{key}:</b> {value}\n"
            text += "\n"

        await message.edit(text, parse_mode="html")

