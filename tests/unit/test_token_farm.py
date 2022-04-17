
from scripts.helpful_scripts import INITIAL_PRICE_FEED_VALUE, LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract
from brownie import network, exceptions
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
import pytest
from scripts.deploy import deploy_token_farm_and_dapp_token

def test_set_price_feed_contract():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    non_owner = get_account(index=1)
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    price_feed_address = get_contract("eth_usd_price_feed")
    token_farm.setPriceFeedContract(dapp_token.address, price_feed_address, {"from": account})
    
    assert token_farm.tokenPriceFeedMapping(dapp_token.address) == price_feed_address

    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setPriceFeedContract(dapp_token.address, price_feed_address, {"from": non_owner})

def test_stake_tokens(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    dapp_token.approve(token_farm.address, amount_staked, {"from": account})
    token_farm.stakeTokens(amount_staked, dapp_token.address, {"from": account})

    assert (
        token_farm.stakingBalance(dapp_token.address, account.address) == amount_staked
    )
    assert(token_farm.uniqueTokensStaked(account.address) == 1)
    assert(token_farm.stakers(0) == account.address)    
    return token_farm, dapp_token


def test_issue_tokens(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    token_farm, dapp_token = test_stake_tokens(amount_staked)
    starting_balance = dapp_token.balanceOf(account.address)

    token_farm.issueTokens({"from": account})

    # we are staking 1 dapp_token == in price to 1 ETH
    assert(
        dapp_token.balanceOf(account.address) == starting_balance + INITIAL_PRICE_FEED_VALUE
    )
    return token_farm, dapp_token

def test_get_token_value():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()        
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    price_feed_address = get_contract("eth_usd_price_feed")
    token_farm.setPriceFeedContract(dapp_token.address, price_feed_address, {"from": account})

    price, decimals = token_farm.getTokenValue(dapp_token.address)

    assert(price == INITIAL_PRICE_FEED_VALUE)
    assert(decimals == 18)

def test_get_user_single_token_value(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    token_farm, dapp_token = test_stake_tokens(amount_staked)

    single_token_value = token_farm.getUserSingleTokenValue(account, dapp_token.address)
    assert(single_token_value == INITIAL_PRICE_FEED_VALUE)

def test_get_user_total_value(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()    
    token_farm, dapp_token = test_issue_tokens(amount_staked)

    total_value = token_farm.getUserTotalValue(account.address)
    assert(total_value == INITIAL_PRICE_FEED_VALUE)        

def test_unstake_tokens(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()    
    token_farm, dapp_token = test_issue_tokens(amount_staked)

    token_farm.unstakeTokens(dapp_token.address)

    assert token_farm.stakingBalance(dapp_token.address, account.address) == 0
    assert token_farm.uniqueTokensStaked(account.address) == 0