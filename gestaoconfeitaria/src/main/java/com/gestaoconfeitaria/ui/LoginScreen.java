package com.gestaoconfeitaria.ui;

import com.gestaoconfeitaria.db.DatabaseConnection;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.io.*;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class LoginScreen extends JFrame {
    private static final String LAST_EMAIL_FILE = "last_email.txt"; // Arquivo para armazenar o último e-mail
    private JTextField emailField;
    private JPasswordField passwordField;
    private boolean passwordVisible = false; // Define se a senha está visível

    public LoginScreen() {
        // Configurações da tela
        setTitle("Tela de Login");
        setSize(400, 250);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null); // Centraliza a janela
        setResizable(false);  // Evita redimensionamento

        // Painel principal
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

        GridBagConstraints gbc = new GridBagConstraints();
        gbc.fill = GridBagConstraints.HORIZONTAL;
        gbc.insets = new Insets(5, 5, 5, 5);

        // Componentes
        JLabel emailLabel = new JLabel("E-mail:");
        emailLabel.setFont(new Font("Arial", Font.PLAIN, 14));
        gbc.gridx = 0;
        gbc.gridy = 0;
        panel.add(emailLabel, gbc);

        emailField = new JTextField(20);  // Campo ajustado para ter tamanho adequado
        emailField.setPreferredSize(new Dimension(200, 30));
        cargarUltimoEmail(); // Preenche o último e-mail informado
        gbc.gridx = 1;
        panel.add(emailField, gbc);

        JLabel passwordLabel = new JLabel("Senha:");
        passwordLabel.setFont(new Font("Arial", Font.PLAIN, 14));
        gbc.gridx = 0;
        gbc.gridy = 1;
        panel.add(passwordLabel, gbc);

        passwordField = new JPasswordField(20);
        passwordField.setPreferredSize(new Dimension(200, 30));
        gbc.gridx = 1;
        gbc.gridy = 1;
        panel.add(passwordField, gbc);

        JButton eyeButton = new JButton("\uD83D\uDC41"); // Usando Unicode para ícone de olho
        eyeButton.setPreferredSize(new Dimension(50, 30));
        eyeButton.setBorder(BorderFactory.createEmptyBorder());
        eyeButton.addActionListener(e -> togglePasswordVisibility());
        gbc.gridx = 2;
        gbc.gridy = 1;
        panel.add(eyeButton, gbc);

        JButton loginButton = new JButton("Entrar");
        loginButton.setFont(new Font("Arial", Font.BOLD, 14));
        gbc.gridx = 0;
        gbc.gridy = 2;
        gbc.gridwidth = 2;
        gbc.anchor = GridBagConstraints.CENTER;
        loginButton.addActionListener(e -> autenticarUsuario());
        panel.add(loginButton, gbc);

        add(panel);
    }

    private void togglePasswordVisibility() {
        // Alterna entre mostrar e esconder a senha
        passwordField.setEchoChar(passwordVisible ? '•' : (char) 0); // Mostra ou esconde
        passwordVisible = !passwordVisible;
    }

    private void cargarUltimoEmail() {
        try (BufferedReader reader = new BufferedReader(new FileReader(LAST_EMAIL_FILE))) {
            String lastEmail = reader.readLine();
            if (lastEmail != null) {
                emailField.setText(lastEmail);
            }
        } catch (IOException e) {
            // Caso o arquivo não exista, não faz nada
            System.err.println("Nenhum e-mail salvo anteriormente.");
        }
    }

    private void salvarUltimoEmail(String email) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(LAST_EMAIL_FILE))) {
            writer.write(email);
        } catch (IOException e) {
            System.err.println("Erro ao salvar o último e-mail: " + e.getMessage());
        }
    }

    private void autenticarUsuario() {
        String email = emailField.getText();
        String senha = new String(passwordField.getPassword());

        try (Connection connection = DatabaseConnection.connect()) {
            String sql = "SELECT * FROM tb_usuario WHERE email = ? AND senha_hash = ?";
            PreparedStatement statement = connection.prepareStatement(sql);
            statement.setString(1, email);
            statement.setString(2, senha);

            ResultSet resultSet = statement.executeQuery();
            if (resultSet.next()) {
                JOptionPane.showMessageDialog(this, "Login bem-sucedido!");
                salvarUltimoEmail(email); // Salva o e-mail após login bem-sucedido
                dispose(); // Fecha a tela de login
                MainScreen.abrirTelaPrincipal(); // Abre a Tela Principal
            } else {
                JOptionPane.showMessageDialog(this, "E-mail ou senha inválidos.", "Erro", JOptionPane.ERROR_MESSAGE);
            }
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Erro ao autenticar: " + ex.getMessage(), "Erro", JOptionPane.ERROR_MESSAGE);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            LoginScreen loginScreen = new LoginScreen();
            loginScreen.setVisible(true);
        });
    }
}