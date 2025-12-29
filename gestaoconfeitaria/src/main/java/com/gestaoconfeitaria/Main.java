package com.gestaoconfeitaria;

import com.gestaoconfeitaria.db.DatabaseConnection;

import java.sql.Connection;

public class Main {
    public static void main(String[] args) {
        try (Connection connection = DatabaseConnection.connect()) {
            System.out.println("Conexão com o banco de dados realizada com sucesso!");
        } catch (Exception e) {
            System.err.println("Erro: " + e.getMessage());
        }
    }
}