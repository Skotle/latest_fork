ServerEvents.commandRegistry(event => {
  const { commands: Commands } = event;

  event.register(
    Commands.literal('rules') // Command name: /rules
      .executes(ctx => {
        const player = ctx.source.player; // Get the player who ran the command
        if (!player) return 0; // Fail if not a player (e.g., console)

        // Send rules as chat messages with formatting
        player.displayClientMessage(Component.gold("=== 서버 규칙 ==="), false);
        player.displayClientMessage(Component.white("1. 다른 플레이어로부터 비방하거나 물건을 훔치지 마세요."), false);
        player.displayClientMessage(Component.white("2. 부정행위, 해킹 또는 버그 악용을 금지합니다."), false);
        player.displayClientMessage(Component.white("3. 빌드를 적절하고 지연 친화적으로 유지하세요."), false);
        player.displayClientMessage(Component.white("4. 어떤 것에 대한 규칙이 여기에 나열되어 있지 않다고 해서 괜찮다는 의미는 아니므로 상식적으로 생각해보세요!"), false);
        player.displayClientMessage(Component.gold('==================='), false);

        return 1; // Success
      })
  );
});


