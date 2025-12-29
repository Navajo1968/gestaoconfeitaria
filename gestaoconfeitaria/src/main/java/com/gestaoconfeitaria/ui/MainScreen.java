package com.gestaoconfeitaria.ui;

import javax.swing.*;
import java.awt.*;

public class MainScreen extends JFrame {

    public MainScreen() {
        // Configurar a janela principal
        setTitle("Gestão de Confeitaria - Tela Principal");
        setSize(800, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null); // Centraliza na tela
        setResizable(false); // Desativa redimensionamento

        // Criar a barra de menu
        JMenuBar menuBar = new JMenuBar();

        // Menu "Cadastro"
        JMenu menuCadastro = new JMenu("Cadastro");
        JMenuItem menuItemUsuario = new JMenuItem("Usuário");
        menuItemUsuario.addActionListener(event -> abrirTelaCadastroUsuario());  // Chamada corrigida
        menuCadastro.add(menuItemUsuario);

        // Menu "Sair"
        JMenu menuSair = new JMenu("Sair");
        JMenuItem menuItemSair = new JMenuItem("Fechar");
        menuItemSair.addActionListener(e -> {
            int confirm = JOptionPane.showConfirmDialog(this, "Deseja realmente sair?", "Confirmar Saída", JOptionPane.YES_NO_OPTION);
            if (confirm == JOptionPane.YES_OPTION) {
                System.exit(0); // Fecha a aplicação
            }
        });
        menuSair.add(menuItemSair);

        // Adicionar menus à barra
        menuBar.add(menuCadastro);
        menuBar.add(menuSair);

        // Configurar a barra de menu na janela
        setJMenuBar(menuBar);

        // Conteúdo principal (bem-vindo)
        JLabel labelBemVindo = new JLabel("Bem-vindo ao Sistema de Gestão de Confeitaria!", SwingConstants.CENTER);
        labelBemVindo.setFont(new Font("Arial", Font.BOLD, 16));
        add(labelBemVindo, BorderLayout.CENTER);
    }

    private void abrirTelaCadastroUsuario() {
        // Abrir a tela de cadastro de usuário
        SwingUtilities.invokeLater(() -> {
            CadastroUsuarioScreen telaCadastro = new CadastroUsuarioScreen();
            telaCadastro.setVisible(true);
        });
    }

    public static void abrirTelaPrincipal() {
        SwingUtilities.invokeLater(() -> {
            MainScreen mainScreen = new MainScreen();
            mainScreen.setVisible(true);
        });
    }

    public static void main(String[] args) {
        abrirTelaPrincipal(); // Somente para testes
    }
}