package com.gestaoconfeitaria.ui;

import com.gestaoconfeitaria.db.DatabaseConnection;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class LoginScreen extends JFrame {
    private JTextField emailField;
    private JPasswordField passwordField;

    public LoginScreen() {
        // Configurações da tela
        setTitle("Tela de Login");
        setSize(400, 250);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null); // Centraliza a janela

        // Painel principal
        JPanel panel = new JPanel(new GridLayout(3, 2, 10, 10));
        panel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

        // Componentes
        JLabel emailLabel = new JLabel("E-mail:");
        emailField = new JTextField();

        JLabel passwordLabel = new JLabel("Senha:");
        passwordField = new JPasswordField();

        JButton loginButton = new JButton("Entrar");

        // Adiciona os componentes ao painel
        panel.add(emailLabel);
        panel.add(emailField);
        panel.add(passwordLabel);
        panel.add(passwordField);
        panel.add(new JLabel()); // Espaço vazio
        panel.add(loginButton);

        // Adiciona o painel à janela
        add(panel);

        // Ação do botão de login
        loginButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                autenticarUsuario();
            }
        });
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
                // Aqui você pode abrir a tela principal depois do login
                dispose(); // Fecha a tela de login
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