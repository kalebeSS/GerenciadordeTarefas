import os
import sqlite3

class GerenciadorDeTarefas:
    def __init__(self) -> None:
        self.conexao_banco = sqlite3.connect('banco_gerenciador.db')
        self.cursor = self.conexao_banco.cursor()

    def cria_tabela(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            tarefa TEXT NOT NULL,
            concluida INTEGER NOT NULL CHECK (concluida IN (0, 1))
        )''')
        self.conexao_banco.commit()

    def inicia_projeto(self):
        self.cria_tabela()
        while True:
            op = self.escreve_introducao()
            if op == 'fechar':
                break
            
            elif op == 'adicionar':
                tarefa = input('Qual a tarefa: ')
                self.adicionar_tarefa(tarefa)
                
            elif op == 'visualizar':
                self.visualizar_tarefa()
                
            elif op == 'remover':
                self.visualizar_tarefa()
                tarefa_id = input('Digite o ID da tarefa que deseja remover: ')
                self.remover_tarefa(tarefa_id)
            elif op == 'concluir':
                self.visualizar_tarefa()
                tarefa_id = input('Digite o ID da tarefa que deseja marcar como concluída: ')
                self.marcar_tarefa_concluida(tarefa_id)
            elif op == 'salvar':
                self.salvar_tarefa()

            else:
                print('Opção inválida. Tente novamente.')

    def escreve_introducao(self):
        print('Bem Vindo ao Gerenciador de Tarefas pessoal\n')
        print('O que deseja fazer?\n')
        print('adicionar tarefa\n')
        print('visualizar tarefa\n')
        print('remover tarefa\n')
        print('concluir tarefa\n')
        print('salvar tarefa\n')
        print('fechar projeto\n')
        op = input("Escolha escrevendo apenas o primeiro nome: ")
        os.system('cls' if os.name == 'nt' else 'clear')
        return op

    def adicionar_tarefa(self, tarefa):
        self.cursor.execute('INSERT INTO tarefas (tarefa, concluida) VALUES (?, 0)', (tarefa,))
        self.conexao_banco.commit()
        print('Tarefa adicionada com sucesso.')

    def visualizar_tarefa(self):
        self.cursor.execute('SELECT * FROM tarefas')
        tarefas = self.cursor.fetchall()
        if tarefas:
            for tarefa in tarefas:
                status = 'Concluída' if tarefa[2] else 'Pendente'
                print(f'ID: {tarefa[0]}, Tarefa: {tarefa[1]}, Status: {status}')
        else:
            print('Nenhuma tarefa encontrada.')

    def remover_tarefa(self, tarefa_id):
        self.cursor.execute('DELETE FROM tarefas WHERE id = ?', (tarefa_id,))
        self.conexao_banco.commit()
        print(f'Tarefa com ID {tarefa_id} removida com sucesso.')

    def marcar_tarefa_concluida(self, tarefa_id):
        self.cursor.execute('UPDATE tarefas SET concluida = 1 WHERE id = ?', (tarefa_id,))
        self.conexao_banco.commit()
        print(f'Tarefa com ID {tarefa_id} marcada como concluída.')

    def salvar_tarefa(self):
        self.cursor.execute('SELECT * FROM tarefas')
        tarefas = self.cursor.fetchall()
        with open('tarefas.txt', 'w') as file:
            for tarefa in tarefas:
                status = 'Concluída' if tarefa[2] else 'Pendente'
                file.write(f'ID: {tarefa[0]}, Tarefa: {tarefa[1]}, Status: {status}\n')
        print('Tarefas salvas em tarefas.txt.')


if __name__ == "__main__":
    projeto = GerenciadorDeTarefas()
    projeto.inicia_projeto()
