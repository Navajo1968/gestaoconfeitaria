package com.gestaoconfeitaria.ui;

import javax.swing.*;
import java.awt.event.ActionEvent;

// Corrigir nome para coincidir com o arquivo
public class CadastroUsuarioScreen extends JFrame {

    // Declarar serialVersionUID para evitar o aviso.
    private static final long serialVersionUID = 1L;

    public CadastroUsuarioScreen() {
        // Configuração inicial da janela
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

        // Adiciona ação para abrir a tela de cadastro de usuário
        menuItemUsuario.addActionListener(this::abrirTelaCadastroUsuario);

        menuCadastro.add(menuItemUsuario);

        // Menu "Sair"
        JMenu menuSair = new JMenu("Sair");
        JMenuItem menuItemSair = new JMenuItem("Fechar");
        menuItemSair.addActionListener(e -> {
            int confirm = JOptionPane.showConfirmDialog(this, "Deseja realmente sair?", "Confirmar Saída", JOptionPane.YES_NO_OPTION);
            if (confirm == JOptionPane.YES_OPTION) {
                System.exit(0);
            }
        });
        menuSair.add(menuItemSair);

        // Adicionar menus à barra
        menuBar.add(menuCadastro);
        menuBar.add(menuSair);

        // Configurar a barra de menu na janela
        setJMenuBar(menuBar);

        // Mensagem de boas-vindas
        JLabel labelBemVindo = new JLabel("Bem-vindo ao Sistema de Gestão de Confeitaria!", SwingConstants.CENTER);
        labelBemVindo.setFont(labelBemVindo.getFont().deriveFont(16.0f));
        add(labelBemVindo);
    }

    private void abrirTelaCadastroUsuario(ActionEvent event) {
        // Abrir a tela de cadastro de usuários
        SwingUtilities.invokeLater(() -> {
            CadastroUsuarioScreen telaCadastroUsuario = new CadastroUsuarioScreen();
            telaCadastroUsuario.setVisible(true);
        });
    }

    // Método estático para inicialização da tela principal
    public static void abrirTelaPrincipal() {
        SwingUtilities.invokeLater(() -> {
            CadastroUsuarioScreen mainScreen = new CadastroUsuarioScreen();
            mainScreen.setVisible(true);
        });
    }

    public static void main(String[] args) {
        abrirTelaPrincipal(); // Chama o método estático para abrir
    }
}