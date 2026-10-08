data remove storage desert_ball:capture stack
data remove storage desert_ball:capture uuid
$data modify storage desert_ball:capture stack set from storage desert_ball:vault accounts.p$(owner).stack
$data modify storage desert_ball:capture uuid set from storage desert_ball:vault accounts.p$(owner).uuid
