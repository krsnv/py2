import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTableView,
    QPushButton,
    QLineEdit,
    QFormLayout,
    QMessageBox,
    QDialog,
    QDialogButtonBox,
    QComboBox,
    QTabWidget,
)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel


class TeacherForm(QDialog):
    def __init__(self, parent=None, teacher_id=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить/Редактировать Учителя")
        self.setGeometry(100, 100, 300, 150)

        self.teacher_id = teacher_id
        self.name_input = QLineEdit()
        self.subject_input = QLineEdit()
        self.group_input = QComboBox()

        layout = QFormLayout()
        layout.addRow("ФИО:", self.name_input)
        layout.addRow("Предмет:", self.subject_input)
        layout.addRow("Группа:", self.group_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

        if teacher_id:
            self.load_data()

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def load_data(self):
        query = QSqlQuery()
        query.prepare("SELECT name, subject, group_name FROM Teachers WHERE id = :id")
        query.bindValue(":id", self.teacher_id)
        query.exec_()
        if query.next():
            self.name_input.setText(query.value(0))
            self.subject_input.setText(query.value(1))
            self.group_input.setCurrentText(query.value(2))

    def get_data(self):
        return {
            "name": self.name_input.text(),
            "subject": self.subject_input.text(),
            "group": self.group_input.currentText(),
        }


class GroupForm(QDialog):
    def __init__(self, parent=None, group_id=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить/Редактировать Группу")
        self.setGeometry(100, 100, 300, 100)

        self.group_id = group_id
        self.name_input = QLineEdit()

        layout = QFormLayout()
        layout.addRow("Имя группы:", self.name_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

        if group_id:
            self.load_data()

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def load_data(self):
        query = QSqlQuery()
        query.prepare("SELECT name FROM Groups WHERE id = :id")
        query.bindValue(":id", self.group_id)
        query.exec_()
        if query.next():
            self.name_input.setText(query.value(0))

    def get_data(self):
        return {"name": self.name_input.text()}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление Учителями и Группами")
        self.setGeometry(100, 100, 800, 600)

        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName("teachers.db")
        if not self.database.open():
            QMessageBox.critical(
                self, "Ошибка базы данных", "Не удалось подключиться к базе данных."
            )
            sys.exit(1)

        self.create_tables()

        self.teacher_model = QSqlQueryModel()
        self.group_model = QSqlQueryModel()
        self.load_teacher_data()
        self.load_group_data()

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.teacher_tab = QWidget()
        self.group_tab = QWidget()

        self.tab_widget.addTab(self.teacher_tab, "Учителя")
        self.tab_widget.addTab(self.group_tab, "Группы")

        self.setup_teacher_tab()
        self.setup_group_tab()

        self.tab_widget.setCurrentIndex(0)

    def create_tables(self):
        query = QSqlQuery()
        query.exec_(
            """CREATE TABLE IF NOT EXISTS Teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            subject TEXT NOT NULL,
            group_name TEXT NOT NULL
        )"""
        )
        query.exec_(
            """CREATE TABLE IF NOT EXISTS Groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )"""
        )

    def load_teacher_data(self):
        query = QSqlQuery()
        query.exec_("SELECT id, name, subject, group_name FROM Teachers")
        self.teacher_model.setQuery(query)

    def load_group_data(self):
        query = QSqlQuery()
        query.exec_("SELECT id, name FROM Groups")
        self.group_model.setQuery(query)

    def setup_teacher_tab(self):
        self.teacher_view = QTableView()
        self.teacher_view.setModel(self.teacher_model)
        self.teacher_view.setSelectionBehavior(QTableView.SelectRows)

        self.teacher_filter = QLineEdit()
        self.teacher_filter.setPlaceholderText("Введите ФИО для фильтрации")
        self.teacher_filter.textChanged.connect(self.filter_teachers)

        self.add_teacher_button = QPushButton("Добавить Учителя")
        self.edit_teacher_button = QPushButton("Редактировать Учителя")
        self.delete_teacher_button = QPushButton("Удалить Учителя")

        self.add_teacher_button.clicked.connect(self.add_teacher)
        self.edit_teacher_button.clicked.connect(self.edit_teacher)
        self.delete_teacher_button.clicked.connect(self.delete_teacher)

        layout = QVBoxLayout()
        layout.addWidget(self.teacher_filter)
        layout.addWidget(self.teacher_view)
        layout.addWidget(self.add_teacher_button)
        layout.addWidget(self.edit_teacher_button)
        layout.addWidget(self.delete_teacher_button)

        self.teacher_tab.setLayout(layout)

    def filter_teachers(self):
        filter_text = self.teacher_filter.text()
        query = QSqlQuery()
        query.prepare(
            "SELECT id, name, subject, group_name FROM Teachers WHERE name LIKE :filter"
        )
        query.bindValue(":filter", f"%{filter_text}%")
        query.exec_()
        self.teacher_model.setQuery(query)

    def setup_group_tab(self):
        self.group_view = QTableView()
        self.group_view.setModel(self.group_model)
        self.group_view.setSelectionBehavior(QTableView.SelectRows)

        self.add_group_button = QPushButton("Добавить Группу")
        self.edit_group_button = QPushButton("Редактировать Группу")
        self.delete_group_button = QPushButton("Удалить Группу")

        self.add_group_button.clicked.connect(self.add_group)
        self.edit_group_button.clicked.connect(self.edit_group)
        self.delete_group_button.clicked.connect(self.delete_group)

        layout = QVBoxLayout()
        layout.addWidget(self.group_view)
        layout.addWidget(self.add_group_button)
        layout.addWidget(self.edit_group_button)
        layout.addWidget(self.delete_group_button)

        self.group_tab.setLayout(layout)

    def add_teacher(self):
        form = TeacherForm(self)
        query = QSqlQuery("SELECT name FROM Groups")
        while query.next():
            form.group_input.addItem(query.value(0))

        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            query = QSqlQuery()
            query.prepare(
                "INSERT INTO Teachers (name, subject, group_name) VALUES (:name, :subject, :group_name)"
            )
            query.bindValue(":name", data["name"])
            query.bindValue(":subject", data["subject"])
            query.bindValue(":group_name", data["group"])
            query.exec_()
            self.load_teacher_data()

    def edit_teacher(self):
        selected = self.teacher_view.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите учителя для редактирования.")
            return

        teacher_id = selected[0].data()
        form = TeacherForm(self, teacher_id)
        query = QSqlQuery("SELECT name FROM Groups")
        while query.next():
            form.group_input.addItem(query.value(0))

        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            query = QSqlQuery()
            query.prepare(
                "UPDATE Teachers SET name = :name, subject = :subject, group_name = :group_name WHERE id = :id"
            )
            query.bindValue(":name", data["name"])
            query.bindValue(":subject", data["subject"])
            query.bindValue(":group_name", data["group"])
            query.bindValue(":id", teacher_id)
            query.exec_()
            self.load_teacher_data()

    def delete_teacher(self):
        selected = self.teacher_view.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите учителя для удаления.")
            return

        teacher_id = selected[0].data()
        query = QSqlQuery()
        query.prepare("DELETE FROM Teachers WHERE id = :id")
        query.bindValue(":id", teacher_id)
        query.exec_()
        self.load_teacher_data()

    def add_group(self):
        form = GroupForm(self)
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            query = QSqlQuery()
            query.prepare("INSERT INTO Groups (name) VALUES (:name)")
            query.bindValue(":name", data["name"])
            query.exec_()
            self.load_group_data()

    def edit_group(self):
        selected = self.group_view.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите группу для редактирования.")
            return

        group_id = selected[0].data()
        form = GroupForm(self, group_id)
        if form.exec_() == QDialog.Accepted:
            data = form.get_data()
            query = QSqlQuery()
            query.prepare("UPDATE Groups SET name = :name WHERE id = :id")
            query.bindValue(":name", data["name"])
            query.bindValue(":id", group_id)
            query.exec_()
            self.load_group_data()

    def delete_group(self):
        selected = self.group_view.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите группу для удаления.")
            return

        group_id = selected[0].data()
        query = QSqlQuery()
        query.prepare("DELETE FROM Groups WHERE id = :id")
        query.bindValue(":id", group_id)
        query.exec_()
        self.load_group_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
