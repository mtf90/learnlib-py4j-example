package com.github.mtf90;

import py4j.GatewayServer;

public class Main {

    public static void main(String[] args) {
        GatewayServer server = new GatewayServer();
        server.start();
    }
}
