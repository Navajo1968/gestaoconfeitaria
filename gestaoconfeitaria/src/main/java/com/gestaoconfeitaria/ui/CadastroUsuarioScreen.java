package com.gestaoconfeitaria.ui;

import com.gestaoconfeitaria.db.DatabaseConnection;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.sql.*;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class CadastroUsuarioScreen extends JFrame {
    // Componentes da interface gráfica
    private JTextField nomeField;
    private JTextField emailField;
    private JTextField telefoneField;
    private JPasswordField senhaField;
    private JTable usuariosTable;
    private DefaultTableModel tableModel;

    public CadastroUsuarioScreen() {
        // Configuração inicial da janela
        setTitle("Cadastro de Usuários");
        setSize(900, 600);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setLayout(new BorderLayout());

        // Painel do formulário de cadastro
        JPanel formPanel = new JPanel(new GridLayout(5, 2, 10, 10));
        formPanel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

        formPanel.add(new JLabel("Nome:"));
        nomeField = new JTextField();
        formPanel.add(nomeField);

        formPanel.add(new JLabel("E-mail:"));
        emailField = new JTextField();
        formPanel.add(emailField);

        formPanel.add(new JLabel("Telefone:"));
        telefoneField = new JTextField();
        formPanel.add(telefoneField);

        formPanel.add(new JLabel("Senha:"));
        senhaField = new JPasswordField();
        formPanel.add(senhaField);

        JButton salvarButton = new JButton("Salvar");
        salvarButton.addActionListener(this::salvarUsuario);
        formPanel.add(salvarButton);

        JButton atualizarButton = new JButton("Atualizar");
        atualizarButton.addActionListener(e -> carregarUsuarios());
        formPanel.add(atualizarButton);

        add(formPanel, BorderLayout.NORTH);

        // Tabela para exibir os registros de usuários
        tableModel = new DefaultTableModel(new String[]{
                "ID", "Nome", "E-mail", "Telefone",
                "Validade Senha", "Data Criação", "Último Acesso", "Última Alteração", "Status"
        }, 0);
        usuariosTable = new JTable(tableModel);
        usuariosTable.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);

        JScrollPane tableScrollPane = new JScrollPane(usuariosTable);
        add(tableScrollPane, BorderLayout.CENTER);

        // Painel de botões para edição
        JPanel buttonPanel = new JPanel();
        JButton editarButton = new JButton("Editar");
        editarButton.addActionListener(this::editarUsuario);
        buttonPanel.add(editarButton);

        JButton excluirButton = new JButton("Excluir");
        excluirButton.addActionListener(this::excluirUsuario);
        buttonPanel.add(excluirButton);

        add(buttonPanel, BorderLayout.SOUTH);

        carregarUsuarios(); // Carregar dados ao abrir a tela
    }

    private void salvarUsuario(ActionEvent event) {
        String nome = nomeField.getText().trim();
        String email = emailField.getText().trim();
        String telefone = telefoneField.getText().trim();
        String senha = new String(senhaField.getPassword()).trim();

        if (nome.isEmpty() || email.isEmpty() || senha.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Campos Nome, E-mail e Senha são obrigatórios.", "Erro", JOptionPane.ERROR_MESSAGE);
            return;
        }

        if (!validarSenha(senha)) {
            JOptionPane.showMessageDialog(this, "A senha deve ter entre 8 e 20 caracteres, com pelo menos 1 letra maiúscula, 1 número e 1 caractere especial.", "Erro", JOptionPane.ERROR_MESSAGE);
            return;
        }

        // Hash da senha
        String senhaHash = gerarHashSenha(senha);
        if (senhaHash == null) {
            JOptionPane.showMessageDialog(this, "Erro ao processar a senha.", "Erro", JOptionPane.ERROR_MESSAGE);
            return;
        }

        try (Connection connection = DatabaseConnection.connect()) {
            String sql = "INSERT INTO tb_usuario (nome, email, telefone, senha_hash, status, dt_validade_senha, dt_hr_inclusao) VALUES (?, ?, ?, ?, ?, ?, ?)";
            PreparedStatement statement = connection.prepareStatement(sql);

            // Calculando datas
            LocalDate dataAtual = LocalDate.now();
            LocalDate validadeSenha = dataAtual.plusDays(60); // Data atual + 60 dias
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");

            statement.setString(1, nome);
            statement.setString(2, email);
            statement.setString(3, telefone);
            statement.setString(4, senhaHash); // Armazena o hash da senha
            statement.setString(5, "Ativo"); // Status padrão "Ativo"
            statement.setString(6, validadeSenha.format(formatter)); // Validade Senha
            statement.setString(7, dataAtual.format(formatter));     // Data de Inclusão
            statement.executeUpdate();

            JOptionPane.showMessageDialog(this, "Usuário salvo com sucesso!");
            limparFormulario();
            carregarUsuarios();
        } catch (SQLException ex) {
            JOptionPane.showMessageDialog(this, "Erro ao salvar usuário: " + ex.getMessage(), "Erro", JOptionPane.ERROR_MESSAGE);
        }
    }

    private boolean validarSenha(String senha) {
        // Regex para validar senha
        String regex = "^(?=.*[A-Z])(?=.*[\\W_])(?=.*\\d)[\\w\\W]{8,20}$";
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(senha);
        return matcher.matches();
    }

    private String gerarHashSenha(String senha) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] hashBytes = md.digest(senha.getBytes());
            StringBuilder sb = new StringBuilder();
            for (byte b : hashBytes) {
                sb.append(String.format("%02x", b));
            }
            return sb.toString();
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
            return null;
        }
    }

    private void carregarUsuarios() {
        try (Connection connection = DatabaseConnection.connect()) {
            String sql = "SELECT id_usuario, nome, email, telefone, status, dt_validade_senha, dt_hr_inclusao, dt_hr_ultimo_acesso, dt_hr_alteracao FROM tb_usuario";
            Statement statement = connection.createStatement();
            ResultSet resultSet = statement.executeQuery(sql);

            tableModel.setRowCount(0); // Limpar tabela
            while (resultSet.next()) {
                tableModel.addRow(new Object[]{
                        resultSet.getInt("id_usuario"),
                        resultSet.getString("nome"),
                        resultSet.getString("email"),
                        resultSet.getString("telefone"),
                        resultSet.getString("status"), // Mantido na tabela para visualização
                        resultSet.getDate("dt_validade_senha"),
                        resultSet.getTimestamp("dt_hr_inclusao"),
                        resultSet.getTimestamp("dt_hr_ultimo_acesso"),
                        resultSet.getTimestamp("dt_hr_alteracao")
                });
            }
        } catch (SQLException ex) {
            JOptionPane.showMessageDialog(this, "Erro ao carregar usuários: " + ex.getMessage(), "Erro", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void limparFormulario() {
        nomeField.setText("");
        emailField.setText("");
        telefoneField.setText("");
        senhaField.setText("");
    }

    private void editarUsuario(ActionEvent event) {
        int selectedRow = usuariosTable.getSelectedRow();
        if (selectedRow == -1) {
            JOptionPane.showMessageDialog(this, "Selecione um usuário para editar.", "Aviso", JOptionPane.WARNING_MESSAGE);
            return;
        }

        int usuarioId = (int) tableModel.getValueAt(selectedRow, 0);
        String novoNome = JOptionPane.showInputDialog(this, "Digite o novo nome:", tableModel.getValueAt(selectedRow, 1));
        String novoEmail = JOptionPane.showInputDialog(this, "Digite o novo e-mail:", tableModel.getValueAt(selectedRow, 2));
        String novoTelefone = JOptionPane.showInputDialog(this, "Digite o novo telefone:", tableModel.getValueAt(selectedRow, 3));

        try (Connection connection = DatabaseConnection.connect()) {
            String sql = "UPDATE tb_usuario SET nome = ?, email = ?, telefone = ?, dt_hr_alteracao = ? WHERE id_usuario = ?";
            PreparedStatement statement = connection.prepareStatement(sql);

            statement.setString(1, novoNome);
            statement.setString(2, novoEmail);
            statement.setString(3, novoTelefone);
            statement.setTimestamp(4, Timestamp.valueOf(LocalDate.now().atStartOfDay()));
            statement.setInt(5, usuarioId);

            statement.executeUpdate();
            JOptionPane.showMessageDialog(this, "Usuário atualizado com sucesso!");
            carregarUsuarios();
        } catch (SQLException ex) {
            JOptionPane.showMessageDialog(this, "Erro ao atualizar usuário: " + ex.getMessage(), "Erro", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void excluirUsuario(ActionEvent event) {
        int selectedRow = usuariosTable.getSelectedRow();
        if (selectedRow == -1) {
            JOptionPane.showMessageDialog(this, "Selecione um usuário para excluir.", "Aviso", JOptionPane.WARNING_MESSAGE);
            return;
        }

        int usuarioId = (int) tableModel.getValueAt(selectedRow, 0);
        int confirm = JOptionPane.showConfirmDialog(this, "Deseja realmente excluir o usuário?", "Confirmação", JOptionPane.YES_NO_OPTION);
        if (confirm != JOptionPane.YES_OPTION) return;

        try (Connection connection = DatabaseConnection.connect()) {
            String sql = "DELETE FROM tb_usuario WHERE id_usuario = ?";
            PreparedStatement statement = connection.prepareStatement(sql);
            statement.setInt(1, usuarioId);
            statement.executeUpdate();

            JOptionPane.showMessageDialog(this, "Usuário excluído com sucesso!");
            carregarUsuarios();
        } catch (SQLException ex) {
            JOptionPane.showMessageDialog(this, "Erro ao excluir usuário: " + ex.getMessage(), "Erro", JOptionPane.ERROR_MESSAGE);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            CadastroUsuarioScreen cadastroUsuarioScreen = new CadastroUsuarioScreen();
            cadastroUsuarioScreen.setVisible(true);
        });
    }
}